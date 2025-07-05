#!/usr/bin/env python3
"""
Test script for easy-slam package.
"""

def test_import():
    """Test basic import functionality."""
    try:
        import easy_slam
        print("✓ easy_slam module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import easy_slam: {e}")
        return False

def test_easy_slam_class():
    """Test EasySLAM class initialization."""
    try:
        from easy_slam import EasySLAM
        slam = EasySLAM()
        print("✓ EasySLAM class initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize EasySLAM: {e}")
        return False

def test_sensors():
    """Test sensor imports."""
    try:
        from easy_slam.sensors import WebcamSensor, RealSenseSensor
        print("✓ Sensor classes imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import sensors: {e}")
        return False

def test_algorithms():
    """Test algorithm imports."""
    try:
        from easy_slam.algorithms import ORBSLAM, FastSLAM, GraphSLAM
        print("✓ Algorithm classes imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import algorithms: {e}")
        return False

def test_utils():
    """Test utility imports."""
    try:
        from easy_slam.utils import load_config, save_trajectory
        print("✓ Utility functions imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import utilities: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing easy-slam package...")
    print("=" * 40)
    
    tests = [
        test_import,
        test_easy_slam_class,
        test_sensors,
        test_algorithms,
        test_utils
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! easy-slam package is working correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 