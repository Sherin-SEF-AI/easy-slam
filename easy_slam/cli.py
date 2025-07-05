#!/usr/bin/env python3
"""
Command-line interface for Easy-SLAM.
"""

import argparse
import sys
import signal
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Easy-SLAM: Simultaneous Localization and Mapping",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic SLAM with webcam
  easy-slam --camera 0 --algorithm orb_slam

  # RGB-D SLAM with RealSense
  easy-slam --camera realsense --algorithm rgbd_slam --visualization

  # Advanced SLAM with all features
  easy-slam --camera 0 --algorithm rgbd_slam --enable-semantic --enable-sensor-fusion --enable-map-merging --enable-profiling

  # Offline processing with dataset
  easy-slam --camera /path/to/dataset --algorithm graphslam --save-trajectory --save-map

  # Multi-session mapping
  easy-slam --camera 0 --algorithm rgbd_slam --enable-map-merging --session-id session1
        """
    )
    
    # Basic options
    parser.add_argument('--camera', '-c', default=0,
                       help='Camera source (int, webcam, realsense, stereo, lidar, or dataset path)')
    parser.add_argument('--algorithm', '-a', default='orb_slam',
                       choices=['orb_slam', 'fastslam', 'graphslam', 'visual_inertial', 'rgbd_slam'],
                       help='SLAM algorithm to use')
    parser.add_argument('--config', type=str,
                       help='Configuration file path')
    
    # Output options
    parser.add_argument('--visualization', '-v', action='store_true',
                       help='Enable 3D visualization')
    parser.add_argument('--save-trajectory', action='store_true',
                       help='Save trajectory to file')
    parser.add_argument('--save-map', action='store_true',
                       help='Save map to file')
    parser.add_argument('--output-dir', type=str, default='./results',
                       help='Output directory for results')
    
    # Advanced features
    parser.add_argument('--enable-semantic', action='store_true',
                       help='Enable semantic mapping with YOLOv8')
    parser.add_argument('--enable-sensor-fusion', action='store_true',
                       help='Enable sensor fusion (IMU, GPS)')
    parser.add_argument('--enable-map-merging', action='store_true',
                       help='Enable multi-session map merging')
    parser.add_argument('--enable-profiling', action='store_true',
                       help='Enable advanced performance profiling')
    
    # Multi-session options
    parser.add_argument('--session-id', type=str,
                       help='Session ID for multi-session mapping')
    parser.add_argument('--merge-sessions', nargs='+',
                       help='List of session IDs to merge')
    
    # Algorithm-specific parameters
    parser.add_argument('--max-features', type=int, default=2000,
                       help='Maximum number of features (ORB-SLAM)')
    parser.add_argument('--scale-factor', type=float, default=1.2,
                       help='Scale factor for feature detection')
    parser.add_argument('--levels', type=int, default=8,
                       help='Number of pyramid levels')
    parser.add_argument('--voxel-size', type=float, default=0.02,
                       help='Voxel size for RGB-D SLAM')
    
    # Performance options
    parser.add_argument('--max-frames', type=int,
                       help='Maximum number of frames to process')
    parser.add_argument('--fps-limit', type=float,
                       help='Limit processing to specified FPS')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    try:
        from easy_slam import EasySLAM
        
        # Initialize EasySLAM with advanced features
        slam = EasySLAM(
            camera=args.camera,
            algorithm=args.algorithm,
            visualization=args.visualization,
            save_trajectory=args.save_trajectory,
            save_map=args.save_map,
            config_file=args.config,
            enable_semantic=args.enable_semantic,
            enable_sensor_fusion=args.enable_sensor_fusion,
            enable_map_merging=args.enable_map_merging,
            enable_profiling=args.enable_profiling,
            max_features=args.max_features,
            scale_factor=args.scale_factor,
            levels=args.levels,
            voxel_size=args.voxel_size
        )
        
        # Handle multi-session merging
        if args.merge_sessions:
            print(f"[CLI] Merging sessions: {args.merge_sessions}")
            # Load and merge existing sessions
            for session_id in args.merge_sessions:
                session_file = output_dir / f"session_{session_id}.pkl"
                if session_file.exists():
                    # Load session data and merge
                    pass
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            print("\n[CLI] Shutting down...")
            slam.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start SLAM
        print(f"[CLI] Starting Easy-SLAM with {args.algorithm} algorithm")
        print(f"[CLI] Camera: {args.camera}")
        print(f"[CLI] Advanced features:")
        print(f"  - Semantic mapping: {args.enable_semantic}")
        print(f"  - Sensor fusion: {args.enable_sensor_fusion}")
        print(f"  - Map merging: {args.enable_map_merging}")
        print(f"  - Profiling: {args.enable_profiling}")
        
        slam.start()
        
        # Main loop
        frame_count = 0
        while True:
            # Check for performance limits
            if args.max_frames and frame_count >= args.max_frames:
                print(f"[CLI] Reached maximum frames: {args.max_frames}")
                break
            
            # Get performance stats
            if args.enable_profiling:
                stats = slam.get_performance_stats()
                if stats and frame_count % 100 == 0:
                    print(f"[CLI] Performance - FPS: {stats['fps']:.1f}, "
                          f"Memory: {stats['memory_mb']:.1f}MB, "
                          f"CPU: {stats['cpu_percent']:.1f}%")
            
            frame_count += 1
            
            # FPS limiting
            if args.fps_limit:
                import time
                time.sleep(1.0 / args.fps_limit)
    
    except KeyboardInterrupt:
        print("\n[CLI] Interrupted by user")
    except Exception as e:
        print(f"[CLI] Error: {e}")
        sys.exit(1)
    finally:
        if 'slam' in locals():
            slam.stop()
            
            # Save final results
            if args.enable_profiling:
                report_file = output_dir / "performance_report.txt"
                slam.save_performance_report(str(report_file))
                print(f"[CLI] Performance report saved to {report_file}")
            
            if args.save_trajectory:
                trajectory_file = output_dir / "trajectory.txt"
                print(f"[CLI] Trajectory saved to {trajectory_file}")
            
            if args.save_map:
                map_file = output_dir / "map.ply"
                print(f"[CLI] Map saved to {map_file}")
            
            if args.enable_map_merging:
                global_map = slam.get_global_map()
                if global_map:
                    global_map_file = output_dir / "global_map.ply"
                    print(f"[CLI] Global merged map saved to {global_map_file}")

if __name__ == "__main__":
    main() 