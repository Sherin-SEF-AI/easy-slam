"""
Output utilities for trajectory, point cloud, mesh, etc.
"""

import os
import numpy as np
from typing import List, Optional

def save_trajectory(trajectory: List[np.ndarray], path: str, format: str = "tum"):
    """
    Save trajectory to file.
    
    Args:
        trajectory: List of pose matrices
        path: Output file path
        format: Output format ('tum', 'kitti', 'euroc')
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            if format == "tum":
                f.write("# timestamp tx ty tz qx qy qz qw\n")
                for i, pose in enumerate(trajectory):
                    timestamp = i * 0.033  # 30Hz
                    tx, ty, tz = pose[:3, 3]
                    # Convert rotation matrix to quaternion (simplified)
                    qx, qy, qz, qw = 0, 0, 0, 1
                    f.write(f"{timestamp:.6f} {tx:.6f} {ty:.6f} {tz:.6f} {qx:.6f} {qy:.6f} {qz:.6f} {qw:.6f}\n")
            
            elif format == "kitti":
                for pose in trajectory:
                    # KITTI format: 3x4 transformation matrix
                    transform = pose[:3, :4]
                    for row in transform:
                        f.write(" ".join(f"{val:.6f}" for val in row) + "\n")
            
            elif format == "euroc":
                f.write("# timestamp, p_RS_R_x [m], p_RS_R_y [m], p_RS_R_z [m], q_RS_w [], q_RS_x [], q_RS_y [], q_RS_z []\n")
                for i, pose in enumerate(trajectory):
                    timestamp = i * 0.033 * 1e9  # nanoseconds
                    tx, ty, tz = pose[:3, 3]
                    qx, qy, qz, qw = 0, 0, 0, 1
                    f.write(f"{int(timestamp)}, {tx:.6f}, {ty:.6f}, {tz:.6f}, {qw:.6f}, {qx:.6f}, {qy:.6f}, {qz:.6f}\n")
        
        print(f"[Output] Saved trajectory to {path} ({format} format)")
        
    except Exception as e:
        print(f"[Output] Error saving trajectory: {e}")

def save_point_cloud(point_cloud: np.ndarray, path: str, format: str = "ply"):
    """
    Save point cloud to file.
    
    Args:
        point_cloud: Point cloud as numpy array (Nx3)
        path: Output file path
        format: Output format ('ply', 'pcd', 'xyz')
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        if format == "ply":
            with open(path, 'w') as f:
                f.write("ply\n")
                f.write("format ascii 1.0\n")
                f.write(f"element vertex {len(point_cloud)}\n")
                f.write("property float x\n")
                f.write("property float y\n")
                f.write("property float z\n")
                f.write("end_header\n")
                
                for point in point_cloud:
                    f.write(f"{point[0]:.6f} {point[1]:.6f} {point[2]:.6f}\n")
        
        elif format == "pcd":
            with open(path, 'w') as f:
                f.write("# .PCD v0.7 - Point Cloud Data file format\n")
                f.write("VERSION 0.7\n")
                f.write("FIELDS x y z\n")
                f.write("SIZES 4 4 4\n")
                f.write("TYPES F F F\n")
                f.write("COUNTS 1 1 1\n")
                f.write(f"WIDTH {len(point_cloud)}\n")
                f.write("HEIGHT 1\n")
                f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
                f.write(f"POINTS {len(point_cloud)}\n")
                f.write("DATA ascii\n")
                
                for point in point_cloud:
                    f.write(f"{point[0]:.6f} {point[1]:.6f} {point[2]:.6f}\n")
        
        elif format == "xyz":
            np.savetxt(path, point_cloud, fmt='%.6f', delimiter=' ')
        
        print(f"[Output] Saved point cloud to {path} ({format} format)")
        
    except Exception as e:
        print(f"[Output] Error saving point cloud: {e}")

def save_mesh(vertices: np.ndarray, faces: Optional[np.ndarray] = None, path: str = "mesh.ply"):
    """
    Save mesh to PLY file.
    
    Args:
        vertices: Vertex coordinates (Nx3)
        faces: Face indices (Mx3) or None for point cloud
        path: Output file path
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(vertices)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            
            if faces is not None:
                f.write(f"element face {len(faces)}\n")
                f.write("property list uchar int vertex_indices\n")
            
            f.write("end_header\n")
            
            # Write vertices
            for vertex in vertices:
                f.write(f"{vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}\n")
            
            # Write faces
            if faces is not None:
                for face in faces:
                    f.write(f"3 {face[0]} {face[1]} {face[2]}\n")
        
        print(f"[Output] Saved mesh to {path}")
        
    except Exception as e:
        print(f"[Output] Error saving mesh: {e}")

def save_occupancy_grid(grid: np.ndarray, path: str, resolution: float = 0.1):
    """
    Save occupancy grid to file.
    
    Args:
        grid: 2D occupancy grid (0=free, 1=occupied, -1=unknown)
        path: Output file path
        resolution: Grid resolution in meters
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save as numpy array
        np.save(path, grid)
        
        # Also save metadata
        meta_path = path.replace('.npy', '_meta.txt')
        with open(meta_path, 'w') as f:
            f.write(f"resolution: {resolution}\n")
            f.write(f"width: {grid.shape[1]}\n")
            f.write(f"height: {grid.shape[0]}\n")
        
        print(f"[Output] Saved occupancy grid to {path}")
        
    except Exception as e:
        print(f"[Output] Error saving occupancy grid: {e}") 