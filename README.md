# EasySLAM

**EasySLAM** is a production-ready Python package that makes Simultaneous Localization and Mapping (SLAM) accessible to beginners while providing advanced features for researchers and professionals.



![image](https://github.com/user-attachments/assets/8b986504-fc43-443b-84df-61869e8fcfb7)


![Screenshot from 2025-07-08 20-15-16](https://github.com/user-attachments/assets/50c5f952-caa5-4659-872d-3e13a446a247)

![Screenshot from 2025-07-08 20-15-09](https://github.com/user-attachments/assets/f98af136-35de-4f3f-9c36-03659f580b42)

![Screenshot from 2025-07-08 20-15-03](https://github.com/user-attachments/assets/c14b86cb-1b00-442d-9aa0-9f0ccedf7be9)



[![PyPI version](https://badge.fury.io/py/easy-slam.svg)](https://badge.fury.io/py/easy-slam)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Features

### Core SLAM Algorithms
- **ORB-SLAM**: Feature-based visual SLAM with loop closure
- **FastSLAM**: Particle filter SLAM for mobile robots
- **GraphSLAM**: Graph optimization-based SLAM
- **Visual-Inertial SLAM**: Camera + IMU fusion
- **RGB-D SLAM**: Depth camera SLAM with Open3D

### Sensor Support
- **Webcam**: Standard USB cameras
- **RealSense**: Intel RealSense depth cameras
- **Stereo Cameras**: Dual camera setups
- **LiDAR**: 3D laser scanners
- **Datasets**: TUM, KITTI, custom datasets

### Advanced Features
- **Semantic Mapping**: Object detection and labeling
- **Sensor Fusion**: Multi-sensor data fusion with EKF
- **Map Merging**: Combine multiple SLAM sessions
- **Performance Profiling**: Real-time monitoring and optimization
- **GUI Interface**: PyQt6-based visualization tool

### Output Formats
- **Trajectory**: TUM format, JSON, CSV
- **Point Clouds**: PLY, PCD formats
- **3D Maps**: Mesh reconstruction
- **Performance Reports**: Detailed analytics

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install easy-slam
```

### From Source
```bash
git clone https://github.com/Sherin-SEF-AI/EasySLAM.git
cd EasySLAM
pip install -e .
```

### Optional Dependencies
```bash
# For 3D visualization
pip install easy-slam[3d]

# For RealSense cameras
pip install easy-slam[realsense]

# For advanced optimization
pip install easy-slam[g2o]

# For development
pip install easy-slam[dev]
```

## 🎯 Quick Start

### Basic Usage
```python
from easy_slam import EasySLAM

# Initialize with webcam
slam = EasySLAM(camera=0, algorithm='orb_slam')
slam.start()
```

### Advanced Usage
```python
from easy_slam import EasySLAM

# Configure with advanced features
slam = EasySLAM(
    camera='realsense',
    algorithm='rgbd_slam',
    semantic_mapping=True,
    sensor_fusion=True,
    save_trajectory=True,
    output_dir='./results'
)

# Start SLAM processing
slam.start()

# Get results
trajectory = slam.get_trajectory()
map_data = slam.get_map()
```

### GUI Interface
```bash
# Launch the GUI
easy-slam-gui

# Or run programmatically
python -m easy_slam.gui
```

## 📖 Documentation

### API Reference

#### EasySLAM Class
```python
class EasySLAM:
    def __init__(self, 
                 camera: Union[int, str] = 0,
                 config: Optional[str] = None,
                 mode: str = 'realtime',
                 algorithm: str = 'orb_slam',
                 visualization: bool = True,
                 save_trajectory: bool = False,
                 output_dir: str = "./results",
                 **kwargs):
        """
        Initialize SLAM system.
        
        Args:
            camera: Camera index, path, or sensor type
            config: Optional path to YAML config file
            mode: 'realtime' or 'offline'
            algorithm: SLAM algorithm name
            visualization: Enable 3D visualization
            save_trajectory: Save trajectory to file
            output_dir: Directory for output files
        """
```

#### Available Algorithms
- `'orb_slam'`: ORB-SLAM (default)
- `'fastslam'`: FastSLAM particle filter
- `'graphslam'`: Graph optimization SLAM
- `'visual_inertial'`: Visual-inertial SLAM
- `'rgbd_slam'`: RGB-D SLAM

#### Available Cameras
- `0, 1, 2...`: Webcam indices
- `'webcam'`: Default webcam
- `'realsense'`: Intel RealSense
- `'stereo'`: Stereo camera setup
- `'lidar'`: LiDAR sensor
- `'path/to/dataset'`: Dataset file or directory

### Configuration

Create a YAML configuration file:
```yaml
slam:
  algorithm: orb_slam
  mode: realtime

sensor:
  type: webcam
  resolution: [640, 480]
  fps: 30

algorithm:
  max_features: 2000
  scale_factor: 1.2
  levels: 8

visualization:
  enabled: true
  update_rate: 10

output:
  save_trajectory: true
  directory: "./results"

performance:
  threading: true
  memory_limit: "2GB"
```

## 🎮 GUI Features

The EasySLAM GUI provides:
- **Real-time video display**
- **2D trajectory visualization**
- **3D map view**
- **Feature point visualization**
- **Performance monitoring**
- **Live log output**
- **Camera and algorithm selection**
- **Advanced feature toggles**

## 🔧 Advanced Features

### Semantic Mapping
```python
slam = EasySLAM(
    camera=0,
    semantic_mapping=True,
    semantic_model='yolov8'
)
```

### Sensor Fusion
```python
slam = EasySLAM(
    camera='realsense',
    sensor_fusion=True,
    imu_enabled=True
)
```

### Map Merging
```python
slam = EasySLAM(
    camera=0,
    map_merging=True,
    loop_closure=True
)
```

## 📊 Performance

EasySLAM is optimized for real-time performance:
- **30+ FPS** on standard webcams
- **Memory efficient** for long sessions
- **Multi-threaded** processing
- **GPU acceleration** support (optional)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/Sherin-SEF-AI/EasySLAM.git
cd EasySLAM
pip install -e .[dev]
pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV for computer vision algorithms
- Open3D for 3D processing
- PyQt6 for GUI framework
- NumPy and SciPy for numerical computing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Sherin-SEF-AI/EasySLAM/issues)
- **Email**: sherin.joseph2217@gmail.com
- **Documentation**: [GitHub Wiki](https://github.com/Sherin-SEF-AI/EasySLAM/wiki)

## 🔗 Links

- **Source Code**: https://github.com/Sherin-SEF-AI/EasySLAM
- **PyPI Package**: https://pypi.org/project/easy-slam/
- **Documentation**: https://github.com/Sherin-SEF-AI/EasySLAM/wiki

---

** sherin joseph roy** 
# Trigger GitHub Pages workflow
