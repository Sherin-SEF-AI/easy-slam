#!/usr/bin/env python3
"""
Demo script for easy-slam package.
This demonstrates the basic functionality with a simple example.
"""

import time
from easy_slam import EasySLAM

def basic_demo():
    """Basic demo showing simple SLAM usage."""
    print("🚀 Easy-SLAM Basic Demo")
    print("=" * 40)
    
    # Create SLAM instance with basic settings
    slam = EasySLAM(
        camera=0,  # Use default webcam
        algorithm='orb_slam',  # Use ORB-SLAM algorithm
        visualization=False,  # Disable 3D visualization for demo
        save_trajectory=True,  # Save trajectory
        output_dir="./demo_results"
    )
    
    print("✓ SLAM system initialized")
    print("Press Ctrl+C to stop the demo")
    
    try:
        # Start SLAM processing
        slam.start()
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo stopped by user")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    finally:
        # Clean up
        slam.stop()
        
        # Show results
        trajectory = slam.get_trajectory()
        map_data = slam.get_map()
        
        print(f"\n📊 Demo Results:")
        print(f"  - Frames processed: {len(trajectory)}")
        print(f"  - Map points: {len(map_data) if map_data is not None else 0}")
        print(f"  - Results saved to: ./demo_results/")

def advanced_demo():
    """Advanced demo showing configuration options."""
    print("\n🚀 Easy-SLAM Advanced Demo")
    print("=" * 40)
    
    # Create SLAM instance with advanced settings
    slam = EasySLAM(
        camera='webcam',
        config='configs/indoor.yaml',  # Use indoor preset
        mode='offline',  # Process in offline mode
        algorithm='fastslam',  # Use FastSLAM algorithm
        visualization=False,
        save_trajectory=True,
        output_dir="./advanced_results",
        # Advanced options
        max_features=3000,
        scale_factor=1.2,
        levels=10
    )
    
    print("✓ Advanced SLAM system initialized")
    print("This demo will process mock data (no real camera)")
    
    try:
        # Start SLAM processing
        slam.start()
        
    except Exception as e:
        print(f"❌ Error during advanced demo: {e}")
    finally:
        # Clean up
        slam.stop()
        
        # Show results
        trajectory = slam.get_trajectory()
        print(f"\n📊 Advanced Demo Results:")
        print(f"  - Frames processed: {len(trajectory)}")
        print(f"  - Results saved to: ./advanced_results/")

def sensor_demo():
    """Demo showing different sensor types."""
    print("\n🚀 Easy-SLAM Sensor Demo")
    print("=" * 40)
    
    sensors = ['webcam', 'realsense', 'stereo', 'lidar']
    
    for sensor_type in sensors:
        print(f"\nTesting {sensor_type} sensor...")
        
        try:
            slam = EasySLAM(
                camera=sensor_type,
                algorithm='orb_slam',
                visualization=False,
                save_trajectory=False
            )
            
            print(f"✓ {sensor_type} sensor initialized successfully")
            slam.stop()
            
        except Exception as e:
            print(f"✗ {sensor_type} sensor failed: {e}")

def main():
    """Run all demos."""
    print("🎯 Easy-SLAM Package Demo")
    print("=" * 50)
    
    # Run basic demo
    basic_demo()
    
    # Run advanced demo
    advanced_demo()
    
    # Run sensor demo
    sensor_demo()
    
    print("\n" + "=" * 50)
    print("🎉 All demos completed!")
    print("\n📚 Next steps:")
    print("  1. Check the demo_results/ and advanced_results/ folders")
    print("  2. Try different algorithms: orb_slam, fastslam, graphslam, visual_inertial")
    print("  3. Experiment with different sensors and configurations")
    print("  4. Read the documentation for more advanced features")

if __name__ == "__main__":
    main() 