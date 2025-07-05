"""
Easy-SLAM: A comprehensive SLAM package for beginners and advanced users.
"""

__version__ = "1.0.0"
__author__ = "Easy-SLAM Team"

from .core import EasySLAM

# Export main class
__all__ = ['EasySLAM']

# Import all algorithms
from .algorithms import (
    ORBSLAM, FastSLAM, GraphSLAM, VisualInertialSLAM, RGBDSLAM
)

# Import all sensors
from .sensors import (
    WebcamSensor, RealSenseSensor, StereoSensor, LiDARSensor, DatasetSensor
)

# Import all utilities
from .utils import (
    calibrate_sensor, load_config, save_trajectory, save_point_cloud, 
    save_mesh, profile_slam, handle_error
)

# Import advanced features
from .utils.semantic import SemanticMapper
from .utils.sensor_fusion import SensorFusion, ExtendedKalmanFilter
from .utils.map_merging import MapMerger, MultiSessionMapper
from .utils.advanced_profiling import PerformanceProfiler, ProfilerContext, profile_module

# Import visualization
from .visualization import Viewer3D 