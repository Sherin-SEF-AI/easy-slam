#!/usr/bin/env python3
"""
Basic usage example for easy-slam.
"""

from easy_slam import EasySLAM

def main():
    # Simple usage - just 2 lines!
    slam = EasySLAM(camera=0)
    slam.start()

if __name__ == "__main__":
    main() 