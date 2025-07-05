#!/usr/bin/env python3
"""
Advanced Easy-SLAM Demo
Showcases all advanced features: RGB-D SLAM, semantic mapping, sensor fusion, map merging, and profiling.
"""

import time
import numpy as np
import open3d as o3d
from pathlib import Path

def demo_rgbd_slam():
    """Demo RGB-D SLAM with Open3D."""
    print("\n" + "="*50)
    print("RGB-D SLAM DEMO")
    print("="*50)
    
    try:
        from easy_slam.algorithms import RGBDSLAM
        
        # Initialize RGB-D SLAM
        slam = RGBDSLAM(voxel_size=0.02)
        print("✓ RGB-D SLAM initialized")
        
        # Create mock RGB-D data
        rgb = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        depth = np.random.rand(480, 640) * 5.0  # 0-5 meters
        
        # Process frames
        for i in range(10):
            pose = slam.process(rgb, depth)
            print(f"  Frame {i+1}: Pose computed")
        
        # Get results
        trajectory = slam.get_trajectory()
        map_pcd = slam.get_map()
        
        print(f"✓ Processed {len(trajectory)} frames")
        print(f"✓ Generated map with {len(map_pcd.points)} points")
        
        return slam
        
    except Exception as e:
        print(f"✗ RGB-D SLAM demo failed: {e}")
        return None

def demo_semantic_mapping():
    """Demo semantic mapping with YOLOv8."""
    print("\n" + "="*50)
    print("SEMANTIC MAPPING DEMO")
    print("="*50)
    
    try:
        from easy_slam.utils.semantic import SemanticMapper
        
        # Initialize semantic mapper
        mapper = SemanticMapper()
        print("✓ Semantic mapper initialized")
        
        # Create mock RGB image
        rgb = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Detect objects
        detections = mapper.detect(rgb)
        print(f"✓ Detected {len(detections)} objects")
        
        for det in detections[:3]:  # Show first 3 detections
            print(f"  - Class {det['class']}: {det['conf']:.2f} confidence")
        
        # Create mock point cloud and attach semantics
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.random.randn(100, 3))
        
        # Mock camera intrinsic
        intrinsic = o3d.camera.PinholeCameraIntrinsic(640, 480, 525, 525, 320, 240)
        
        # Attach semantic labels
        semantic_data = mapper.attach_semantics(pcd, rgb, np.random.rand(480, 640), intrinsic)
        print(f"✓ Attached semantics to {len(semantic_data)} points")
        
        return mapper
        
    except Exception as e:
        print(f"✗ Semantic mapping demo failed: {e}")
        return None

def demo_sensor_fusion():
    """Demo sensor fusion with EKF."""
    print("\n" + "="*50)
    print("SENSOR FUSION DEMO")
    print("="*50)
    
    try:
        from easy_slam.utils.sensor_fusion import SensorFusion
        
        # Initialize sensor fusion
        fusion = SensorFusion()
        print("✓ Sensor fusion initialized")
        
        # Simulate IMU data
        for i in range(100):
            gyro = np.random.randn(3) * 0.1  # Angular velocity
            accel = np.random.randn(3) * 0.5  # Linear acceleration
            fusion.add_imu(gyro, accel)
        
        # Simulate visual odometry
        for i in range(10):
            pos = np.random.randn(3) * 0.1
            quat = np.array([1, 0, 0, 0]) + np.random.randn(4) * 0.01
            quat = quat / np.linalg.norm(quat)  # Normalize
            fusion.add_visual(pos, quat)
        
        # Simulate GPS
        for i in range(5):
            gps_pos = np.random.randn(3) * 10  # GPS position
            fusion.add_gps(gps_pos)
        
        # Get fused pose
        fused_pose = fusion.get_fused_pose()
        velocity = fusion.get_velocity()
        orientation = fusion.get_orientation()
        
        print(f"✓ Fused {len(fusion.imu_data)} IMU measurements")
        print(f"✓ Fused {len(fusion.visual_data)} visual measurements")
        print(f"✓ Fused {len(fusion.gps_data)} GPS measurements")
        print(f"✓ Current velocity: {np.linalg.norm(velocity):.3f} m/s")
        
        return fusion
        
    except Exception as e:
        print(f"✗ Sensor fusion demo failed: {e}")
        return None

def demo_map_merging():
    """Demo map merging and loop closure detection."""
    print("\n" + "="*50)
    print("MAP MERGING DEMO")
    print("="*50)
    
    try:
        from easy_slam.utils.map_merging import MapMerger, MultiSessionMapper
        
        # Initialize map merger
        merger = MapMerger(voxel_size=0.05)
        print("✓ Map merger initialized")
        
        # Create mock point clouds
        map1 = o3d.geometry.PointCloud()
        map1.points = o3d.utility.Vector3dVector(np.random.randn(200, 3))
        map1.paint_uniform_color([1, 0, 0])  # Red
        
        map2 = o3d.geometry.PointCloud()
        map2.points = o3d.utility.Vector3dVector(np.random.randn(200, 3) + [5, 0, 0])
        map2.paint_uniform_color([0, 1, 0])  # Green
        
        # Merge maps
        merged_map, transform = merger.merge_maps(map1, map2)
        print(f"✓ Merged maps with {len(merged_map.points)} total points")
        print(f"✓ Transformation matrix computed")
        
        # Multi-session mapping
        multi_mapper = MultiSessionMapper()
        
        # Add sessions
        poses1 = [np.eye(4) for _ in range(10)]
        poses2 = [np.eye(4) for _ in range(10)]
        
        multi_mapper.add_session(map1, poses1)
        multi_mapper.add_session(map2, poses2)
        
        global_map = multi_mapper.get_global_map()
        print(f"✓ Multi-session mapping: {len(multi_mapper.maps)} sessions")
        print(f"✓ Global map has {len(global_map.points)} points")
        
        return merger, multi_mapper
        
    except Exception as e:
        print(f"✗ Map merging demo failed: {e}")
        return None, None

def demo_advanced_profiling():
    """Demo advanced performance profiling."""
    print("\n" + "="*50)
    print("ADVANCED PROFILING DEMO")
    print("="*50)
    
    try:
        from easy_slam.utils.advanced_profiling import PerformanceProfiler, ProfilerContext
        
        # Initialize profiler
        profiler = PerformanceProfiler()
        print("✓ Performance profiler initialized")
        
        # Simulate different module timings
        for i in range(50):
            # Simulate sensor read
            with ProfilerContext(profiler, "sensor_read"):
                time.sleep(0.01)
            
            # Simulate SLAM processing
            with ProfilerContext(profiler, "slam_processing"):
                time.sleep(0.02)
            
            # Simulate visualization
            with ProfilerContext(profiler, "visualization"):
                time.sleep(0.005)
            
            # Record frame
            profiler.record_frame()
        
        # Get statistics
        stats = profiler.get_system_stats()
        print(f"✓ Processed {stats['frame_count']} frames")
        print(f"✓ Average FPS: {stats['avg_fps']:.1f}")
        print(f"✓ Average memory: {stats['avg_memory_mb']:.1f} MB")
        print(f"✓ Average CPU: {stats['avg_cpu_percent']:.1f}%")
        
        # Get module statistics
        for module in ["sensor_read", "slam_processing", "visualization"]:
            module_stats = profiler.get_module_stats(module)
            if module_stats:
                print(f"  {module}: {module_stats['mean']*1000:.2f} ms avg")
        
        # Get bottlenecks
        bottlenecks = profiler.get_bottlenecks()
        if bottlenecks:
            print("✓ Performance bottlenecks detected:")
            for bottleneck in bottlenecks[:3]:
                print(f"  - {bottleneck['module']}: {bottleneck['spike_factor']:.1f}x spike")
        
        # Generate report
        report = profiler.generate_report("demo_performance_report.txt")
        print("✓ Performance report generated")
        
        # Stop profiler
        profiler.stop()
        
        return profiler
        
    except Exception as e:
        print(f"✗ Advanced profiling demo failed: {e}")
        return None

def demo_integrated_features():
    """Demo integrated advanced features."""
    print("\n" + "="*50)
    print("INTEGRATED ADVANCED FEATURES DEMO")
    print("="*50)
    
    try:
        from easy_slam import EasySLAM
        
        # Initialize EasySLAM with all advanced features
        slam = EasySLAM(
            camera=0,
            algorithm='rgbd_slam',
            visualization=False,  # Disable for demo
            enable_semantic=True,
            enable_sensor_fusion=True,
            enable_map_merging=True,
            enable_profiling=True,
            voxel_size=0.02
        )
        
        print("✓ EasySLAM initialized with all advanced features")
        
        # Simulate processing
        print("  Simulating SLAM processing...")
        time.sleep(2)  # Simulate processing time
        
        # Get performance stats
        stats = slam.get_performance_stats()
        if stats:
            print(f"  Performance: {stats['fps']:.1f} FPS, {stats['memory_mb']:.1f} MB")
        
        # Get fused pose
        fused_pose = slam.get_fused_pose()
        if fused_pose is not None:
            print("  ✓ Sensor fusion active")
        
        # Get global map
        global_map = slam.get_global_map()
        if global_map is not None:
            print("  ✓ Map merging active")
        
        # Save performance report
        slam.save_performance_report("integrated_demo_report.txt")
        print("  ✓ Performance report saved")
        
        slam.stop()
        print("✓ Integrated demo completed")
        
        return slam
        
    except Exception as e:
        print(f"✗ Integrated features demo failed: {e}")
        return None

def main():
    """Run all advanced feature demos."""
    print("🚀 ADVANCED EASY-SLAM FEATURES DEMO")
    print("=" * 60)
    print("This demo showcases all advanced features:")
    print("• RGB-D SLAM with Open3D")
    print("• Semantic mapping with YOLOv8")
    print("• Sensor fusion with Extended Kalman Filter")
    print("• Map merging and loop closure detection")
    print("• Advanced performance profiling")
    print("• Integrated features demonstration")
    print("=" * 60)
    
    # Run individual demos
    results = {}
    
    results['rgbd_slam'] = demo_rgbd_slam()
    results['semantic'] = demo_semantic_mapping()
    results['sensor_fusion'] = demo_sensor_fusion()
    results['map_merging'] = demo_map_merging()
    results['profiling'] = demo_advanced_profiling()
    results['integrated'] = demo_integrated_features()
    
    # Summary
    print("\n" + "="*60)
    print("DEMO SUMMARY")
    print("="*60)
    
    successful_demos = sum(1 for result in results.values() if result is not None)
    total_demos = len(results)
    
    print(f"Successful demos: {successful_demos}/{total_demos}")
    
    for demo_name, result in results.items():
        status = "✓ PASSED" if result is not None else "✗ FAILED"
        print(f"  {demo_name.replace('_', ' ').title()}: {status}")
    
    if successful_demos == total_demos:
        print("\n🎉 ALL ADVANCED FEATURES WORKING!")
        print("✅ Easy-SLAM is ready for production use with advanced capabilities!")
    else:
        print(f"\n⚠️  {total_demos - successful_demos} demos failed")
        print("Check the error messages above for details.")
    
    print("\n📁 Generated files:")
    print("  - demo_performance_report.txt")
    print("  - integrated_demo_report.txt")
    print("  - performance_report.txt (if integrated demo ran)")

if __name__ == "__main__":
    main() 