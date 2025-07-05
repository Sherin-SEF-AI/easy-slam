from ..core import EasySLAM

def test_easy_slam_init():
    slam = EasySLAM(camera=0)
    assert slam.camera == 0
    assert slam.mode == 'realtime'

def test_easy_slam_start():
    slam = EasySLAM(camera=1)
    # For now, just test that start() doesn't raise an exception
    slam.start() 