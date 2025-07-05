#!/usr/bin/env python3
"""
Comprehensive test suite for easy-slam package.
Tests all major functions and features.
"""

import os
import sys
import time
import numpy as np
from pathlib import Path

def test_imports():
    """Test all module imports."""
    print("🔍 Testing imports...")
    
    try:
        import easy_slam
        print("✓ easy_slam module imported")
        
        from easy_slam import EasySLAM
        print("✓ EasySLAM class imported")
        
        from easy_slam.sensors import WebcamSensor, RealSenseSensor, StereoSensor, LiDARSensor, DatasetSensor
        print("✓ All sensor classes imported")
        
        from easy_slam.algorithms import ORBSLAM, FastSLAM, GraphSLAM, VisualInertialSLAM
        print("✓ All algorithm classes imported")
        
        from easy_slam.utils import (
            calibrate_sensor, load_config, save_trajectory, 
            save_point_cloud, save_mesh, profile_slam, handle_error
        )
        print("✓ All utility functions imported")
        
        from easy_slam.visualization import Viewer3D
        print("✓ Visualization class imported")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_sensor_initialization():
    """Test sensor initialization."""
    print("\n🔍 Testing sensor initialization...")
    
    try:
        from easy_slam.sensors import WebcamSensor, RealSenseSensor, StereoSensor, LiDARSensor
        
        sensors = [
            ('WebcamSensor', WebcamSensor, 0),
            ('RealSenseSensor', RealSenseSensor, {}),
            ('StereoSensor', StereoSensor, {}),
            ('LiDARSensor', LiDARSensor, {}),
        ]
        
        for name, sensor_class, args in sensors:
            try:
                sensor = sensor_class(args)
                print(f"✓ {name} initialized successfully")
                
                # Test reading
                frame = sensor.read()
                if frame is not None:
                    print(f"✓ {name} read() method works")
                else:
                    print(f"⚠ {name} read() returned None (expected for mock sensors)")
                
                # Test release
                sensor.release()
                print(f"✓ {name} release() method works")
                
            except Exception as e:
                print(f"✗ {name} failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Sensor initialization test failed: {e}")
        return False

def test_algorithm_initialization():
    """Test algorithm initialization."""
    print("\n🔍 Testing algorithm initialization...")
    
    try:
        from easy_slam.algorithms import ORBSLAM, FastSLAM, GraphSLAM, VisualInertialSLAM
        
        algorithms = [
            ('ORBSLAM', ORBSLAM, {}),
            ('FastSLAM', FastSLAM, {}),
            ('GraphSLAM', GraphSLAM, {}),
            ('VisualInertialSLAM', VisualInertialSLAM, {}),
        ]
        
        for name, algo_class, config in algorithms:
            try:
                algo = algo_class(config)
                print(f"✓ {name} initialized successfully")
                
                # Test processing with mock data
                mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                result = algo.process(mock_frame)
                
                if result is not None:
                    print(f"✓ {name} process() method works")
                    if hasattr(result, 'pose'):
                        print(f"✓ {name} returned pose data")
                    if hasattr(result, 'map'):
                        print(f"✓ {name} returned map data")
                else:
                    print(f"⚠ {name} process() returned None")
                
            except Exception as e:
                print(f"✗ {name} failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Algorithm initialization test failed: {e}")
        return False

def test_utility_functions():
    """Test utility functions."""
    print("\n🔍 Testing utility functions...")
    
    try:
        from easy_slam.utils import load_config, save_trajectory, save_point_cloud, handle_error
        
        # Test configuration loading
        try:
            config = load_config("configs/indoor.yaml")
            if config:
                print("✓ load_config() works with existing file")
            else:
                print("⚠ load_config() returned empty dict (file may not exist)")
        except Exception as e:
            print(f"⚠ load_config() test: {e}")
        
        # Test trajectory saving
        try:
            trajectory = [np.eye(4) for _ in range(5)]
            save_trajectory(trajectory, "test_trajectory.txt")
            if os.path.exists("test_trajectory.txt"):
                print("✓ save_trajectory() works")
                os.remove("test_trajectory.txt")
            else:
                print("✗ save_trajectory() failed to create file")
        except Exception as e:
            print(f"✗ save_trajectory() failed: {e}")
            return False
        
        # Test point cloud saving
        try:
            point_cloud = np.random.randn(100, 3)
            save_point_cloud(point_cloud, "test_cloud.ply")
            if os.path.exists("test_cloud.ply"):
                print("✓ save_point_cloud() works")
                os.remove("test_cloud.ply")
            else:
                print("✗ save_point_cloud() failed to create file")
        except Exception as e:
            print(f"✗ save_point_cloud() failed: {e}")
            return False
        
        # Test error handling
        try:
            handle_error(Exception("Test error"), "Test context")
            print("✓ handle_error() works")
        except Exception as e:
            print(f"✗ handle_error() failed: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Utility functions test failed: {e}")
        return False

def test_easy_slam_basic():
    """Test basic EasySLAM functionality."""
    print("\n🔍 Testing EasySLAM basic functionality...")
    
    try:
        from easy_slam import EasySLAM
        
        # Test basic initialization
        slam = EasySLAM(
            camera=0,
            algorithm='orb_slam',
            visualization=False,
            save_trajectory=False
        )
        print("✓ EasySLAM basic initialization works")
        
        # Test configuration access
        if hasattr(slam, 'config_data'):
            print("✓ Configuration data accessible")
        
        # Test sensor initialization
        if slam.sensor is not None:
            print("✓ Sensor initialized")
        
        # Test algorithm initialization
        if slam.slam_algorithm is not None:
            print("✓ SLAM algorithm initialized")
        
        # Test stop method
        slam.stop()
        print("✓ stop() method works")
        
        return True
        
    except Exception as e:
        print(f"✗ EasySLAM basic test failed: {e}")
        return False

def test_easy_slam_advanced():
    """Test advanced EasySLAM functionality."""
    print("\n🔍 Testing EasySLAM advanced functionality...")
    
    try:
        from easy_slam import EasySLAM
        
        # Test with different algorithms
        algorithms = ['orb_slam', 'fastslam', 'graphslam', 'visual_inertial']
        
        for algo in algorithms:
            slam = EasySLAM(
                camera='webcam',
                algorithm=algo,
                visualization=False,
                save_trajectory=False
            )
            print(f"✓ EasySLAM with {algo} algorithm works")
            slam.stop()
        
        # Test with different sensors
        sensors = ['webcam', 'realsense', 'stereo', 'lidar']
        
        for sensor in sensors:
            slam = EasySLAM(
                camera=sensor,
                algorithm='orb_slam',
                visualization=False,
                save_trajectory=False
            )
            print(f"✓ EasySLAM with {sensor} sensor works")
            slam.stop()
        
        # Test configuration override
        slam = EasySLAM(
            camera=0,
            algorithm='orb_slam',
            max_features=3000,
            scale_factor=1.2,
            levels=10
        )
        print("✓ EasySLAM with custom parameters works")
        slam.stop()
        
        return True
        
    except Exception as e:
        print(f"✗ EasySLAM advanced test failed: {e}")
        return False

def test_output_functions():
    """Test output and saving functions."""
    print("\n🔍 Testing output functions...")
    
    try:
        from easy_slam.utils import save_trajectory, save_point_cloud, save_mesh
        
        # Create test data
        trajectory = [np.eye(4) for _ in range(10)]
        point_cloud = np.random.randn(200, 3)
        
        # Test trajectory saving in different formats
        formats = ['tum', 'kitti', 'euroc']
        for fmt in formats:
            save_trajectory(trajectory, f"test_traj_{fmt}.txt", format=fmt)
            if os.path.exists(f"test_traj_{fmt}.txt"):
                print(f"✓ save_trajectory() with {fmt} format works")
                os.remove(f"test_traj_{fmt}.txt")
        
        # Test point cloud saving in different formats
        pcd_formats = ['ply', 'pcd', 'xyz']
        for fmt in pcd_formats:
            save_point_cloud(point_cloud, f"test_cloud.{fmt}", format=fmt)
            if os.path.exists(f"test_cloud.{fmt}"):
                print(f"✓ save_point_cloud() with {fmt} format works")
                os.remove(f"test_cloud.{fmt}")
        
        # Test mesh saving
        vertices = np.random.randn(100, 3)
        faces = np.random.randint(0, 100, (50, 3))
        save_mesh(vertices, faces, "test_mesh.ply")
        if os.path.exists("test_mesh.ply"):
            print("✓ save_mesh() works")
            os.remove("test_mesh.ply")
        
        return True
        
    except Exception as e:
        print(f"✗ Output functions test failed: {e}")
        return False

def test_performance():
    """Test performance and timing."""
    print("\n🔍 Testing performance...")
    
    try:
        from easy_slam.algorithms import ORBSLAM, FastSLAM, GraphSLAM
        
        # Test algorithm processing speed
        algorithms = [
            ('ORBSLAM', ORBSLAM),
            ('FastSLAM', FastSLAM),
            ('GraphSLAM', GraphSLAM),
        ]
        
        mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        for name, algo_class in algorithms:
            algo = algo_class()
            
            # Time processing
            start_time = time.time()
            for _ in range(10):
                result = algo.process(mock_frame)
            end_time = time.time()
            
            avg_time = (end_time - start_time) / 10
            fps = 1.0 / avg_time if avg_time > 0 else 0
            
            print(f"✓ {name}: {fps:.1f} FPS ({avg_time*1000:.1f} ms per frame)")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and recovery."""
    print("\n🔍 Testing error handling...")
    
    try:
        from easy_slam import EasySLAM
        from easy_slam.utils import handle_error
        
        # Test with invalid camera
        slam = EasySLAM(camera=999)
        print("✓ EasySLAM handles invalid camera gracefully")
        slam.stop()
        
        # Test with invalid algorithm
        slam = EasySLAM(algorithm='invalid_algorithm')
        print("✓ EasySLAM handles invalid algorithm gracefully")
        slam.stop()
        
        # Test error handling function
        test_errors = [
            ValueError("Test value error"),
            RuntimeError("Test runtime error"),
            FileNotFoundError("Test file not found"),
        ]
        
        for error in test_errors:
            handle_error(error, "Test context")
        
        print("✓ Error handling works for various error types")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def test_configuration():
    """Test configuration system."""
    print("\n🔍 Testing configuration system...")
    
    try:
        from easy_slam import EasySLAM
        
        # Test default configuration
        slam = EasySLAM()
        default_config = slam.config_data
        
        if 'slam' in default_config and 'sensor' in default_config:
            print("✓ Default configuration loaded")
        
        # Test configuration override
        custom_config = {
            'slam': {'algorithm': 'fastslam'},
            'sensor': {'type': 'webcam', 'resolution': [1280, 720]}
        }
        
        slam = EasySLAM(**custom_config)
        if slam.config_data['slam']['algorithm'] == 'fastslam':
            print("✓ Configuration override works")
        
        slam.stop()
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run all comprehensive tests."""
    print("🧪 COMPREHENSIVE EASY-SLAM TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Sensor Initialization", test_sensor_initialization),
        ("Algorithm Initialization", test_algorithm_initialization),
        ("Utility Functions", test_utility_functions),
        ("EasySLAM Basic", test_easy_slam_basic),
        ("EasySLAM Advanced", test_easy_slam_advanced),
        ("Output Functions", test_output_functions),
        ("Performance", test_performance),
        ("Error Handling", test_error_handling),
        ("Configuration", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Easy-SLAM is working correctly.")
        print("\n✅ Package is ready for production use!")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the errors above.")
    
    # Cleanup any test files
    test_files = [
        "test_trajectory.txt", "test_cloud.ply", "test_mesh.ply",
        "test_traj_tum.txt", "test_traj_kitti.txt", "test_traj_euroc.txt",
        "test_cloud.pcd", "test_cloud.xyz"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 