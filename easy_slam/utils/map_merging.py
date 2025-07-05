import numpy as np
import open3d as o3d
from scipy.spatial import cKDTree

class MapMerger:
    """
    Map merging using ICP and loop closure detection.
    """
    def __init__(self, voxel_size=0.05):
        """
        Args:
            voxel_size: Voxel size for point cloud downsampling
        """
        self.voxel_size = voxel_size
        self.loop_closures = []

    def merge_maps(self, map1, map2, initial_transform=None):
        """
        Merge two point cloud maps using ICP.
        Args:
            map1: First point cloud (Open3D PointCloud)
            map2: Second point cloud (Open3D PointCloud)
            initial_transform: Initial guess for transformation (4x4 matrix)
        Returns:
            merged_map: Merged point cloud
            transform: Transformation from map2 to map1
        """
        # Downsample point clouds
        map1_down = map1.voxel_down_sample(self.voxel_size)
        map2_down = map2.voxel_down_sample(self.voxel_size)
        
        # Estimate normals
        map1_down.estimate_normals()
        map2_down.estimate_normals()
        
        # ICP registration
        if initial_transform is None:
            initial_transform = np.eye(4)
        
        icp_result = o3d.pipelines.registration.registration_icp(
            map2_down, map1_down, 0.1, initial_transform,
            o3d.pipelines.registration.TransformationEstimationPointToPoint()
        )
        
        # Apply transformation to map2
        map2_transformed = map2.transform(icp_result.transformation)
        
        # Merge point clouds
        merged_map = map1 + map2_transformed
        
        # Remove duplicates
        merged_map = merged_map.voxel_down_sample(self.voxel_size)
        
        return merged_map, icp_result.transformation

    def detect_loop_closure(self, current_map, map_database, threshold=0.1):
        """
        Detect loop closure between current map and map database.
        Args:
            current_map: Current point cloud
            map_database: List of previous maps
            threshold: Distance threshold for loop closure
        Returns:
            loop_closure: (map_index, transform) if found, None otherwise
        """
        current_down = current_map.voxel_down_sample(self.voxel_size)
        current_down.estimate_normals()
        
        best_score = float('inf')
        best_transform = None
        best_index = -1
        
        for i, prev_map in enumerate(map_database):
            prev_down = prev_map.voxel_down_sample(self.voxel_size)
            prev_down.estimate_normals()
            
            # Try ICP registration
            try:
                icp_result = o3d.pipelines.registration.registration_icp(
                    current_down, prev_down, threshold, np.eye(4),
                    o3d.pipelines.registration.TransformationEstimationPointToPoint()
                )
                
                if icp_result.fitness > 0.3:  # Good match
                    score = icp_result.inlier_rmse
                    if score < best_score:
                        best_score = score
                        best_transform = icp_result.transformation
                        best_index = i
            except:
                continue
        
        if best_index >= 0:
            return (best_index, best_transform)
        return None

    def optimize_pose_graph(self, poses, loop_closures):
        """
        Optimize pose graph using loop closures.
        Args:
            poses: List of poses
            loop_closures: List of (i, j, transform) tuples
        Returns:
            optimized_poses: Optimized pose list
        """
        # Create pose graph
        pose_graph = o3d.pipelines.registration.PoseGraph()
        
        # Add nodes
        for pose in poses:
            pose_graph.nodes.append(
                o3d.pipelines.registration.PoseGraphNode(pose)
            )
        
        # Add edges (sequential poses)
        for i in range(len(poses) - 1):
            edge = o3d.pipelines.registration.PoseGraphEdge(
                i, i + 1, poses[i + 1] @ np.linalg.inv(poses[i]),
                np.eye(6) * 0.1, uncertain=False
            )
            pose_graph.edges.append(edge)
        
        # Add loop closure edges
        for i, j, transform in loop_closures:
            edge = o3d.pipelines.registration.PoseGraphEdge(
                i, j, transform, np.eye(6) * 0.01, uncertain=True
            )
            pose_graph.edges.append(edge)
        
        # Optimize
        option = o3d.pipelines.registration.GlobalOptimizationOption(
            max_iteration_lm=100,
            max_iteration_levenberg_marquardt=100,
            max_iteration_gauss_newton=100
        )
        
        o3d.pipelines.registration.global_optimization(
            pose_graph,
            o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
            o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(),
            option
        )
        
        # Extract optimized poses
        optimized_poses = []
        for node in pose_graph.nodes:
            optimized_poses.append(node.pose)
        
        return optimized_poses

    def visualize_loop_closures(self, viewer, poses, loop_closures):
        """
        Visualize loop closures in the viewer.
        Args:
            viewer: Open3D visualizer
            poses: List of poses
            loop_closures: List of loop closures
        """
        # Draw trajectory
        trajectory_points = []
        for pose in poses:
            trajectory_points.append(pose[:3, 3])
        
        trajectory_line = o3d.geometry.LineSet()
        trajectory_line.points = o3d.utility.Vector3dVector(trajectory_points)
        trajectory_line.lines = o3d.utility.Vector2iVector(
            [[i, i + 1] for i in range(len(trajectory_points) - 1)]
        )
        trajectory_line.paint_uniform_color([0, 1, 0])  # Green
        
        # Draw loop closures
        loop_lines = []
        loop_colors = []
        
        for i, j, transform in loop_closures:
            start_point = poses[i][:3, 3]
            end_point = poses[j][:3, 3]
            
            loop_lines.append([len(trajectory_points), len(trajectory_points) + 1])
            trajectory_points.extend([start_point, end_point])
            loop_colors.extend([[1, 0, 0], [1, 0, 0]])  # Red
        
        if loop_lines:
            loop_line_set = o3d.geometry.LineSet()
            loop_line_set.points = o3d.utility.Vector3dVector(trajectory_points)
            loop_line_set.lines = o3d.utility.Vector2iVector(loop_lines)
            loop_line_set.paint_uniform_color([1, 0, 0])  # Red
            
            viewer.add_geometry(trajectory_line)
            viewer.add_geometry(loop_line_set)
        else:
            viewer.add_geometry(trajectory_line)

class MultiSessionMapper:
    """
    Multi-session mapping with automatic map merging.
    """
    def __init__(self):
        self.maps = []
        self.poses = []
        self.merger = MapMerger()
        
    def add_session(self, map_pcd, poses):
        """
        Add a new mapping session.
        Args:
            map_pcd: Point cloud map
            poses: List of poses for this session
        """
        if len(self.maps) == 0:
            # First session
            self.maps.append(map_pcd)
            self.poses.extend(poses)
        else:
            # Try to merge with existing maps
            merged = False
            for i, existing_map in enumerate(self.maps):
                loop_closure = self.merger.detect_loop_closure(map_pcd, [existing_map])
                if loop_closure:
                    # Merge maps
                    merged_map, transform = self.merger.merge_maps(
                        existing_map, map_pcd, loop_closure[1]
                    )
                    self.maps[i] = merged_map
                    
                    # Update poses
                    for pose in poses:
                        self.poses.append(transform @ pose)
                    
                    merged = True
                    break
            
            if not merged:
                # No loop closure found, add as new session
                self.maps.append(map_pcd)
                self.poses.extend(poses)
    
    def get_global_map(self):
        """Get the global merged map."""
        if len(self.maps) == 0:
            return None
        elif len(self.maps) == 1:
            return self.maps[0]
        else:
            # Merge all maps
            global_map = self.maps[0]
            for map_pcd in self.maps[1:]:
                global_map, _ = self.merger.merge_maps(global_map, map_pcd)
            return global_map 