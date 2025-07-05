#!/usr/bin/env python3
"""
Advanced usage example for easy-slam.
"""

from easy_slam import EasySLAM

def main():
    # Advanced usage with configuration
    slam = EasySLAM(
        camera="realsense",  # Use RealSense camera
        config="configs/indoor.yaml",  # Load preset config
        mode="offline",  # Process recorded data
        algorithm="orb_slam",  # Use ORB-SLAM
        visualization=True,  # Enable 3D viewer
        save_trajectory=True,  # Save trajectory
        output_dir="./results"  # Output directory
    )
    
    slam.start()

if __name__ == "__main__":
    main() 