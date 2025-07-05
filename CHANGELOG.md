# Changelog

All notable changes to EasySLAM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that will be added in the next release

### Changed
- Changes in existing functionality

### Deprecated
- Features that will be removed in upcoming releases

### Removed
- Features that have been removed

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes

## [0.1.0] - 2024-07-05

### Added
- **Core SLAM System**: Complete EasySLAM class with unified API
- **Multiple SLAM Algorithms**:
  - ORB-SLAM with feature detection and matching
  - FastSLAM particle filter implementation
  - GraphSLAM with pose graph optimization
  - Visual-Inertial SLAM for IMU integration
  - RGB-D SLAM using Open3D
- **Sensor Support**:
  - Webcam sensor with real-time capture
  - RealSense depth camera integration
  - Stereo camera support
  - LiDAR sensor interface
  - Dataset playback (TUM, KITTI formats)
- **Advanced Features**:
  - Semantic mapping with YOLOv8 integration
  - Sensor fusion with Extended Kalman Filter
  - Map merging with ICP and loop closure
  - Advanced performance profiling and monitoring
- **GUI Interface**:
  - PyQt6-based graphical user interface
  - Real-time video display
  - 2D trajectory visualization
  - 3D map view with matplotlib
  - Feature point visualization
  - Performance monitoring dashboard
  - Live log output
- **Output Formats**:
  - Trajectory saving in TUM format
  - Point cloud export (PLY format)
  - Performance reports
  - Session saving and loading
- **CLI Interface**:
  - Command-line tools for easy-slam and easy-slam-gui
  - Configuration file support (YAML)
  - Batch processing capabilities
- **Utility Modules**:
  - Camera calibration tools
  - Configuration management
  - Error handling and logging
  - Output formatting and saving
  - Performance profiling
  - Visualization utilities
- **Testing Framework**:
  - Unit tests for core functionality
  - Integration tests for algorithms
  - Performance benchmarks
- **Documentation**:
  - Comprehensive README with examples
  - API documentation
  - Installation guides
  - Contributing guidelines
  - Changelog

### Technical Features
- **Real-time Performance**: 30+ FPS on standard webcams
- **Memory Management**: Efficient handling of long SLAM sessions
- **Multi-threading**: Background processing for GUI responsiveness
- **Error Handling**: Robust error recovery and logging
- **Modular Architecture**: Pluggable algorithms and sensors
- **Type Hints**: Full type annotation support
- **Cross-platform**: Linux, Windows, macOS support

### Dependencies
- **Core**: numpy, opencv-python, scipy, matplotlib, pyyaml
- **GUI**: PyQt6
- **3D Processing**: open3d (optional)
- **RealSense**: pyrealsense2 (optional)
- **Optimization**: python-g2o (optional)
- **Development**: pytest, sphinx, jupyter, black, flake8

### Initial Release Features
- Production-ready SLAM library
- Beginner-friendly API with advanced capabilities
- Comprehensive documentation and examples
- Professional GUI interface
- Multiple sensor and algorithm support
- Real-time performance optimization
- Extensive testing and validation

---

## Version History

### Version 0.1.0 (Initial Release)
- **Date**: July 5, 2024
- **Author**: sherin joseph roy
- **Email**: sherin.joseph2217@gmail.com
- **GitHub**: https://github.com/Sherin-SEF-AI/EasySLAM

This is the initial release of EasySLAM, providing a complete SLAM solution for robotics and computer vision applications.

---

## Release Notes

### Version 0.1.0 Release Notes

**What's New:**
- Complete SLAM system with 5 different algorithms
- Real-time GUI with advanced visualizations
- Support for multiple sensor types
- Professional documentation and examples
- Production-ready codebase with comprehensive testing

**Key Features:**
- Unified API: `EasySLAM(camera=0).start()`
- GUI Interface: `easy-slam-gui`
- CLI Tools: `easy-slam` command
- Multiple Algorithms: ORB-SLAM, FastSLAM, GraphSLAM, Visual-Inertial, RGB-D
- Sensor Support: Webcam, RealSense, Stereo, LiDAR, Datasets
- Advanced Features: Semantic mapping, sensor fusion, map merging

**System Requirements:**
- Python 3.7 or higher
- OpenCV 4.x
- NumPy, SciPy, Matplotlib
- PyQt6 (for GUI)
- Optional: Open3D, RealSense SDK

**Installation:**
```bash
pip install easy-slam
```

**Quick Start:**
```python
from easy_slam import EasySLAM
slam = EasySLAM(camera=0)
slam.start()
```

**Documentation:**
- [README.md](README.md) - Comprehensive guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [GitHub Repository](https://github.com/Sherin-SEF-AI/EasySLAM)

---

**For detailed information about each release, see the individual release notes on GitHub.** 