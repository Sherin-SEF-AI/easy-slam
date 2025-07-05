#!/usr/bin/env python3
"""
Main entry point for easy-slam unified API.
"""

import os
import time
import threading
from typing import Any, Optional, Dict, Union
import yaml
import numpy as np
import cv2
from pathlib import Path

from .sensors import WebcamSensor, RealSenseSensor, StereoSensor, LiDARSensor, DatasetSensor
from .algorithms import ORBSLAM, FastSLAM, GraphSLAM, VisualInertialSLAM, RGBDSLAM
from .visualization import Viewer3D
from .utils import calibrate_sensor, load_config, save_trajectory, save_point_cloud, save_mesh, profile_slam, handle_error
from .utils.semantic import SemanticMapper
from .utils.sensor_fusion import SensorFusion
from .utils.map_merging import MultiSessionMapper
from .utils.advanced_profiling import PerformanceProfiler

class EasySLAM:
    """
    Unified SLAM interface for beginners and advanced users.
    
    This class provides a simple yet powerful interface for SLAM operations,
    supporting multiple algorithms, sensors, and configuration options.
    """
    
    def __init__(self, 
                 camera: Union[int, str] = 0, 
                 config: Optional[str] = None, 
                 mode: str = 'realtime',
                 algorithm: str = 'orb_slam',
                 visualization: bool = True,
                 save_trajectory: bool = False,
                 output_dir: str = "./results",
                 enable_semantic: bool = False,
                 enable_sensor_fusion: bool = False,
                 enable_map_merging: bool = False,
                 enable_profiling: bool = False,
                 **kwargs):
        """
        Initialize SLAM system.
        
        Args:
            camera: Camera index, path, or sensor type ('webcam', 'realsense', 'stereo', 'lidar')
            config: Optional path to YAML config file
            mode: 'realtime' or 'offline'
            algorithm: SLAM algorithm ('orb_slam', 'fastslam', 'graphslam', 'visual_inertial', 'rgbd_slam')
            visualization: Enable 3D visualization
            save_trajectory: Save trajectory to file
            output_dir: Directory for output files
            enable_semantic: Enable semantic mapping
            enable_sensor_fusion: Enable sensor fusion (IMU, GPS)
            enable_map_merging: Enable multi-session map merging
            enable_profiling: Enable advanced performance profiling
            **kwargs: Additional algorithm-specific parameters
        """
        self.camera = camera
        self.config = config
        self.mode = mode
        self.algorithm = algorithm
        self.visualization = visualization
        self.save_trajectory = save_trajectory
        self.output_dir = output_dir
        self.enable_semantic = enable_semantic
        self.enable_sensor_fusion = enable_sensor_fusion
        self.enable_map_merging = enable_map_merging
        self.enable_profiling = enable_profiling
        self.advanced_options = kwargs
        
        # Initialize components
        self.sensor = None
        self.slam_algorithm = None
        self.viewer = None
        self.running = False
        self.trajectory = []
        self.map_data = None
        
        # Load configuration
        self.config_data = self._load_configuration()
        
        # Initialize sensor
        self._initialize_sensor()
        
        # Initialize SLAM algorithm
        self._initialize_algorithm()
        
        # Initialize advanced features
        self.semantic_mapper = SemanticMapper() if self.enable_semantic else None
        self.sensor_fusion = SensorFusion() if self.enable_sensor_fusion else None
        self.map_merger = MultiSessionMapper() if self.enable_map_merging else None
        self.profiler = PerformanceProfiler() if self.enable_profiling else None
        
        # Initialize visualization
        if self.visualization:
            self._initialize_visualization()
            
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"[easy-slam] Initialized with {self.algorithm} algorithm and {type(self.sensor).__name__}")
    
    def _load_configuration(self) -> Dict:
        """Load configuration from file or use defaults."""
        config_data = {
            'slam': {'algorithm': self.algorithm, 'mode': self.mode},
            'sensor': {'type': 'webcam', 'resolution': [640, 480], 'fps': 30},
            'algorithm': {},
            'visualization': {'enabled': self.visualization, 'update_rate': 10},
            'output': {'save_trajectory': self.save_trajectory, 'directory': self.output_dir},
            'performance': {'threading': True, 'memory_limit': '2GB'}
        }
        
        if self.config and os.path.exists(self.config):
            try:
                with open(self.config, 'r') as f:
                    file_config = yaml.safe_load(f)
                    config_data.update(file_config)
            except Exception as e:
                handle_error(f"Failed to load config file: {e}")
        
        # Override with kwargs
        for key, value in self.advanced_options.items():
            if key in config_data:
                config_data[key].update(value)
            else:
                config_data[key] = value
                
        return config_data
    
    def _initialize_sensor(self):
        """Initialize the appropriate sensor based on configuration."""
        sensor_type = self.config_data['sensor']['type']
        
        try:
            if isinstance(self.camera, int) or self.camera == 'webcam':
                self.sensor = WebcamSensor(self.camera if isinstance(self.camera, int) else 0)
            elif self.camera == 'realsense':
                self.sensor = RealSenseSensor(self.config_data)
            elif self.camera == 'stereo':
                self.sensor = StereoSensor(self.config_data)
            elif self.camera == 'lidar':
                self.sensor = LiDARSensor(self.config_data)
            elif os.path.exists(self.camera):
                self.sensor = DatasetSensor(self.camera)
            else:
                raise ValueError(f"Unsupported sensor type: {self.camera}")
                
        except Exception as e:
            handle_error(f"Failed to initialize sensor: {e}")
            # Fallback to webcam
            self.sensor = WebcamSensor(0)
    
    def _initialize_algorithm(self):
        """Initialize the SLAM algorithm."""
        algorithm_name = self.config_data['slam']['algorithm']
        
        try:
            if algorithm_name == 'orb_slam':
                self.slam_algorithm = ORBSLAM(self.config_data.get('algorithm', {}))
            elif algorithm_name == 'fastslam':
                self.slam_algorithm = FastSLAM(self.config_data.get('algorithm', {}))
            elif algorithm_name == 'graphslam':
                self.slam_algorithm = GraphSLAM(self.config_data.get('algorithm', {}))
            elif algorithm_name == 'visual_inertial':
                self.slam_algorithm = VisualInertialSLAM(self.config_data.get('algorithm', {}))
            elif algorithm_name == 'rgbd_slam':
                self.slam_algorithm = RGBDSLAM(**self.config_data.get('algorithm', {}))
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm_name}")
                
        except Exception as e:
            handle_error(f"Failed to initialize algorithm: {e}")
            # Fallback to ORB-SLAM
            self.slam_algorithm = ORBSLAM()
    
    def _initialize_visualization(self):
        """Initialize 3D visualization."""
        try:
            self.viewer = Viewer3D()
        except Exception as e:
            handle_error(f"Failed to initialize visualization: {e}")
            self.visualization = False
    
    def start(self):
        """Start SLAM processing."""
        if self.running:
            print("[easy-slam] SLAM is already running")
            return
            
        self.running = True
        print(f"[easy-slam] Starting SLAM with camera: {self.camera}")
        
        try:
            if self.mode == 'realtime':
                self._run_realtime()
            else:
                self._run_offline()
        except KeyboardInterrupt:
            print("\n[easy-slam] Stopping SLAM...")
        except Exception as e:
            handle_error(f"SLAM processing error: {e}")
        finally:
            self.stop()
    
    def _run_realtime(self):
        """Run SLAM in real-time mode."""
        frame_count = 0
        start_time = time.time()
        
        while self.running:
            try:
                # Read sensor data
                frame = self.sensor.read()
                if frame is None:
                    continue
                
                # Process with SLAM algorithm
                result = self.slam_algorithm.process(frame)
                
                if result:
                    # Update trajectory
                    if hasattr(result, 'pose'):
                        self.trajectory.append(result.pose)
                    
                    # Update map
                    if hasattr(result, 'map'):
                        self.map_data = result.map
                    
                    # Update visualization
                    if self.visualization and self.viewer:
                        self.viewer.show(self.map_data)
                    
                    # Save trajectory if enabled
                    if self.save_trajectory and len(self.trajectory) % 30 == 0:  # Save every 30 frames
                        self._save_outputs()
                
                frame_count += 1
                
                # Performance monitoring
                if frame_count % 100 == 0:
                    fps = frame_count / (time.time() - start_time)
                    print(f"[easy-slam] FPS: {fps:.2f}, Frames: {frame_count}")
                    
            except Exception as e:
                handle_error(f"Frame processing error: {e}")
                continue
    
    def _run_offline(self):
        """Run SLAM in offline mode."""
        print("[easy-slam] Processing in offline mode...")
        
        while True:
            frame = self.sensor.read()
            if frame is None:
                break
                
            result = self.slam_algorithm.process(frame)
            if result and hasattr(result, 'pose'):
                self.trajectory.append(result.pose)
        
        # Save final outputs
        self._save_outputs()
        print(f"[easy-slam] Offline processing complete. Processed {len(self.trajectory)} frames.")
    
    def _save_outputs(self):
        """Save trajectory and map data."""
        try:
            if self.trajectory:
                trajectory_path = os.path.join(self.output_dir, "trajectory.txt")
                save_trajectory(self.trajectory, trajectory_path)
            
            if self.map_data:
                map_path = os.path.join(self.output_dir, "map.ply")
                save_point_cloud(self.map_data, map_path)
                
        except Exception as e:
            handle_error(f"Failed to save outputs: {e}")
    
    def stop(self):
        """Stop SLAM processing."""
        self.running = False
        
        # Save final outputs
        self._save_outputs()
        
        # Clean up
        if self.sensor:
            self.sensor.release()
        
        print("[easy-slam] SLAM stopped")
    
    def get_trajectory(self):
        """Get the current trajectory."""
        return self.trajectory
    
    def get_map(self):
        """Get the current map data."""
        return self.map_data
    
    def save_results(self, filename: str = None):
        """Save current results to file."""
        if filename is None:
            timestamp = int(time.time())
            filename = f"results_{timestamp}"
        
        try:
            if self.trajectory:
                save_trajectory(self.trajectory, f"{filename}_trajectory.txt")
            
            if self.map_data:
                save_point_cloud(self.map_data, f"{filename}_map.ply")
                
            print(f"[easy-slam] Results saved to {filename}")
            
        except Exception as e:
            handle_error(f"Failed to save results: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def _process_loop(self):
        """Main processing loop."""
        frame_count = 0
        
        while self.running:
            try:
                # Read sensor data
                if self.profiler:
                    self.profiler.start_timer("sensor_read")
                
                sensor_data = self.sensor.read()
                
                if self.profiler:
                    self.profiler.end_timer("sensor_read", self.profiler.start_timer("sensor_read"))
                
                if sensor_data is None:
                    continue
                
                # Process with SLAM algorithm
                if self.profiler:
                    self.profiler.start_timer("slam_processing")
                
                if isinstance(sensor_data, tuple) and len(sensor_data) == 2:
                    # RGB-D data
                    rgb, depth = sensor_data
                    result = self.slam_algorithm.process(rgb, depth)
                else:
                    # Regular image data
                    result = self.slam_algorithm.process(sensor_data)
                
                if self.profiler:
                    self.profiler.end_timer("slam_processing", self.profiler.start_timer("slam_processing"))
                
                if result is not None:
                    # Extract pose and map data
                    pose = result.pose if hasattr(result, 'pose') else result
                    map_data = result.map if hasattr(result, 'map') else None
                    
                    # Store trajectory
                    self.trajectory.append(pose)
                    
                    # Update map data
                    if map_data is not None:
                        self.map_data = map_data
                    
                    # Semantic mapping
                    if self.semantic_mapper and isinstance(sensor_data, tuple):
                        rgb, depth = sensor_data
                        semantic_labels = self.semantic_mapper.detect(rgb)
                        if semantic_labels:
                            print(f"[Semantic] Detected {len(semantic_labels)} objects")
                    
                    # Sensor fusion
                    if self.sensor_fusion:
                        # Extract position and orientation from pose
                        pos = pose[:3, 3]
                        quat = self._matrix_to_quaternion(pose[:3, :3])
                        self.sensor_fusion.add_visual(pos, quat)
                    
                    # Map merging
                    if self.map_merger and self.map_data:
                        self.map_merger.add_session(self.map_data, self.trajectory)
                    
                    # Update visualization
                    if self.viewer:
                        self.viewer.update(pose, self.map_data)
                    
                    # Record frame for profiling
                    if self.profiler:
                        self.profiler.record_frame()
                    
                    frame_count += 1
                    if frame_count % 30 == 0:
                        if self.profiler:
                            stats = self.profiler.get_system_stats()
                            print(f"[easy-slam] Frame {frame_count}, FPS: {stats['fps']:.1f}")
                        else:
                            print(f"[easy-slam] Frame {frame_count}")
                
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                handle_error(e, "SLAM processing loop")
                break

    def _matrix_to_quaternion(self, R):
        """Convert rotation matrix to quaternion."""
        # Simplified conversion - in practice, use proper quaternion library
        trace = np.trace(R)
        if trace > 0:
            S = np.sqrt(trace + 1.0) * 2
            w = 0.25 * S
            x = (R[2, 1] - R[1, 2]) / S
            y = (R[0, 2] - R[2, 0]) / S
            z = (R[1, 0] - R[0, 1]) / S
        else:
            if R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
                S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
                w = (R[2, 1] - R[1, 2]) / S
                x = 0.25 * S
                y = (R[0, 1] + R[1, 0]) / S
                z = (R[0, 2] + R[2, 0]) / S
            elif R[1, 1] > R[2, 2]:
                S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
                w = (R[0, 2] - R[2, 0]) / S
                x = (R[0, 1] + R[1, 0]) / S
                y = 0.25 * S
                z = (R[1, 2] + R[2, 1]) / S
            else:
                S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
                w = (R[1, 0] - R[0, 1]) / S
                x = (R[0, 2] + R[2, 0]) / S
                y = (R[1, 2] + R[2, 1]) / S
                z = 0.25 * S
        
        return np.array([w, x, y, z])

    def get_fused_pose(self):
        """Get fused pose from sensor fusion."""
        if self.sensor_fusion:
            return self.sensor_fusion.get_fused_pose()
        return None

    def get_global_map(self):
        """Get global merged map."""
        if self.map_merger:
            return self.map_merger.get_global_map()
        return self.map_data

    def get_performance_stats(self):
        """Get performance statistics."""
        if self.profiler:
            return self.profiler.get_system_stats()
        return None

    def save_performance_report(self, filename="performance_report.txt"):
        """Save performance report to file."""
        if self.profiler:
            return self.profiler.generate_report(filename)
        return None 