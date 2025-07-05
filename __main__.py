import argparse
from .core import EasySLAM

def main():
    parser = argparse.ArgumentParser(description='easy-slam: Unified SLAM for everyone')
    parser.add_argument('--camera', type=str, default='0', help='Camera index, path, or sensor type')
    parser.add_argument('--config', type=str, help='Path to YAML config file')
    parser.add_argument('--mode', type=str, default='realtime', choices=['realtime', 'offline'], help='SLAM mode')
    args = parser.parse_args()

    slam = EasySLAM(camera=args.camera, config=args.config, mode=args.mode)
    slam.start()

if __name__ == '__main__':
    main() 