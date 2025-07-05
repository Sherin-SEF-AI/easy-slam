import numpy as np
from scipy.linalg import block_diag
import quaternion

class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for sensor fusion.
    Fuses IMU, visual odometry, GPS, and wheel odometry.
    """
    def __init__(self, dt=0.01):
        """
        Args:
            dt: Time step for IMU integration
        """
        self.dt = dt
        # State: [x, y, z, vx, vy, vz, qw, qx, qy, qz, bx, by, bz] (13 states)
        self.state = np.zeros(13)
        self.state[6] = 1.0  # Quaternion w component
        
        # Covariance matrix
        self.P = np.eye(13) * 0.1
        
        # Process noise
        self.Q = np.eye(13) * 0.01
        
        # Measurement noise
        self.R_imu = np.eye(6) * 0.1
        self.R_visual = np.eye(6) * 0.05
        self.R_gps = np.eye(3) * 1.0
        
        # IMU bias
        self.gyro_bias = np.zeros(3)
        self.accel_bias = np.zeros(3)

    def predict(self, gyro, accel):
        """
        Predict step using IMU measurements.
        Args:
            gyro: Angular velocity [wx, wy, wz]
            accel: Linear acceleration [ax, ay, az]
        """
        # Remove bias
        gyro_corrected = gyro - self.gyro_bias
        accel_corrected = accel - self.accel_bias
        
        # Extract current state
        pos = self.state[:3]
        vel = self.state[3:6]
        quat = self.state[6:10]
        
        # Integrate angular velocity
        omega = np.array([0, *gyro_corrected])
        quat_dot = 0.5 * quaternion.as_quat_array(quat) * quaternion.from_rotation_vector(gyro_corrected * self.dt)
        quat_new = quat + quaternion.as_float_array(quat_dot)
        quat_new = quat_new / np.linalg.norm(quat_new)
        
        # Integrate acceleration
        R = quaternion.as_rotation_matrix(quaternion.as_quat_array(quat))
        accel_world = R @ accel_corrected
        accel_world[2] -= 9.81  # Remove gravity
        
        vel_new = vel + accel_world * self.dt
        pos_new = pos + vel * self.dt + 0.5 * accel_world * self.dt**2
        
        # Update state
        self.state[:3] = pos_new
        self.state[3:6] = vel_new
        self.state[6:10] = quat_new
        
        # Update covariance (simplified)
        F = self._compute_jacobian(gyro_corrected, accel_corrected)
        self.P = F @ self.P @ F.T + self.Q

    def update_visual(self, pos_meas, quat_meas):
        """
        Update with visual odometry measurement.
        Args:
            pos_meas: Position measurement [x, y, z]
            quat_meas: Quaternion measurement [qw, qx, qy, qz]
        """
        # Measurement vector
        z = np.concatenate([pos_meas, quat_meas])
        
        # Predicted measurement
        h = np.concatenate([self.state[:3], self.state[6:10]])
        
        # Innovation
        y = z - h
        
        # Measurement matrix
        H = np.zeros((7, 13))
        H[:3, :3] = np.eye(3)
        H[3:7, 6:10] = np.eye(4)
        
        # Kalman gain
        S = H @ self.P @ H.T + self.R_visual
        K = self.P @ H.T @ np.linalg.inv(S)
        
        # Update state and covariance
        self.state += K @ y
        self.state[6:10] = self.state[6:10] / np.linalg.norm(self.state[6:10])  # Normalize quaternion
        self.P = (np.eye(13) - K @ H) @ self.P

    def update_gps(self, gps_pos):
        """
        Update with GPS measurement.
        Args:
            gps_pos: GPS position [lat, lon, alt] or [x, y, z]
        """
        # Measurement matrix
        H = np.zeros((3, 13))
        H[:3, :3] = np.eye(3)
        
        # Innovation
        y = gps_pos - self.state[:3]
        
        # Kalman gain
        S = H @ self.P @ H.T + self.R_gps
        K = self.P @ H.T @ np.linalg.inv(S)
        
        # Update state and covariance
        self.state += K @ y
        self.P = (np.eye(13) - K @ H) @ self.P

    def _compute_jacobian(self, gyro, accel):
        """Compute state transition Jacobian."""
        F = np.eye(13)
        F[:3, 3:6] = np.eye(3) * self.dt
        F[3:6, 6:10] = self._quaternion_jacobian(accel) * self.dt
        return F

    def _quaternion_jacobian(self, accel):
        """Compute quaternion Jacobian for acceleration."""
        # Simplified quaternion Jacobian
        return np.zeros((3, 4))

    def get_pose(self):
        """Get current pose as 4x4 transformation matrix."""
        pos = self.state[:3]
        quat = self.state[6:10]
        R = quaternion.as_rotation_matrix(quaternion.as_quat_array(quat))
        
        pose = np.eye(4)
        pose[:3, :3] = R
        pose[:3, 3] = pos
        return pose

class SensorFusion:
    """
    High-level sensor fusion interface.
    """
    def __init__(self):
        self.ekf = ExtendedKalmanFilter()
        self.imu_data = []
        self.visual_data = []
        self.gps_data = []

    def add_imu(self, gyro, accel, timestamp=None):
        """Add IMU measurement."""
        self.ekf.predict(gyro, accel)
        self.imu_data.append({
            'gyro': gyro, 'accel': accel, 'timestamp': timestamp
        })

    def add_visual(self, pos, quat, timestamp=None):
        """Add visual odometry measurement."""
        self.ekf.update_visual(pos, quat)
        self.visual_data.append({
            'pos': pos, 'quat': quat, 'timestamp': timestamp
        })

    def add_gps(self, pos, timestamp=None):
        """Add GPS measurement."""
        self.ekf.update_gps(pos)
        self.gps_data.append({
            'pos': pos, 'timestamp': timestamp
        })

    def get_fused_pose(self):
        """Get current fused pose."""
        return self.ekf.get_pose()

    def get_velocity(self):
        """Get current velocity."""
        return self.ekf.state[3:6]

    def get_orientation(self):
        """Get current orientation as quaternion."""
        return self.ekf.state[6:10] 