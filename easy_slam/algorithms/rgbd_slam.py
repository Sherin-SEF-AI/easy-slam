import numpy as np
import open3d as o3d
import cv2

class RGBDSLAM:
    """
    Real RGB-D SLAM using Open3D and OpenCV.
    Supports frame-by-frame odometry and map building.
    """
    def __init__(self, intrinsic=None, voxel_size=0.02):
        """
        Args:
            intrinsic: Open3D camera intrinsic (o3d.camera.PinholeCameraIntrinsic)
            voxel_size: Voxel size for map integration
        """
        self.intrinsic = intrinsic or o3d.camera.PinholeCameraIntrinsic(
            640, 480, 525, 525, 320, 240
        )
        self.voxel_size = voxel_size
        self.pose_graph = o3d.pipelines.registration.PoseGraph()
        self.trajectory = []
        self.map = o3d.geometry.PointCloud()
        self.prev_rgbd = None
        self.prev_pose = np.eye(4)
        self.frame_idx = 0
        self.pose_graph.nodes.append(
            o3d.pipelines.registration.PoseGraphNode(np.eye(4))
        )

    def process(self, rgb, depth):
        """
        Process a new RGB-D frame.
        Args:
            rgb: RGB image (numpy array)
            depth: Depth image (numpy array, in meters)
        Returns:
            pose: 4x4 numpy array (camera pose)
        """
        try:
            rgb_o3d = o3d.geometry.Image(cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))
            depth_o3d = o3d.geometry.Image(depth.astype(np.float32))
            rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
                rgb_o3d, depth_o3d, convert_rgb_to_intensity=False
            )
            if self.prev_rgbd is None:
                self.prev_rgbd = rgbd
                self.trajectory.append(self.prev_pose.copy())
                self.frame_idx += 1
                return self.prev_pose.copy()
            odo_init = self.prev_pose.copy()
            option = o3d.pipelines.odometry.OdometryOption()
            success, odo, info = o3d.pipelines.odometry.compute_rgbd_odometry(
                rgbd, self.prev_rgbd, self.intrinsic, odo_init,
                o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(), option
            )
            if not success:
                odo = self.prev_pose.copy()
            self.prev_pose = odo
            self.trajectory.append(odo.copy())
            self.prev_rgbd = rgbd
            # Integrate into map
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
                rgbd, self.intrinsic
            )
            pcd.transform(odo)
            self.map += pcd.voxel_down_sample(self.voxel_size)
            self.frame_idx += 1
            return odo.copy()
        except Exception as e:
            print(f"[RGBDSLAM] Error: {e}")
            return self.prev_pose.copy()

    def get_trajectory(self):
        """Return the list of camera poses (4x4 numpy arrays).
        """
        return self.trajectory

    def get_map(self):
        """Return the accumulated point cloud map (Open3D PointCloud)."""
        return self.map 