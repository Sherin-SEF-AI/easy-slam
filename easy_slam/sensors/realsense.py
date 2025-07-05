"""
RealSense sensor interface with pyrealsense2 support.
"""

import numpy as np
from typing import Optional, Tuple, Dict

class RealSenseSensor:
    """RealSense sensor using pyrealsense2."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize RealSense sensor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.pipeline = None
        self.profile = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the RealSense pipeline."""
        try:
            import pyrealsense2 as rs
            
            # Create pipeline
            self.pipeline = rs.pipeline()
            config = rs.config()
            
            # Configure streams
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            
            # Start pipeline
            self.profile = self.pipeline.start(config)
            
            print("[RealSenseSensor] Initialized RealSense camera")
            
        except ImportError:
            print("[RealSenseSensor] pyrealsense2 not available, using mock data")
            self.pipeline = None
        except Exception as e:
            print(f"[RealSenseSensor] Error initializing RealSense: {e}")
            self.pipeline = None
    
    def read(self) -> Optional[np.ndarray]:
        """
        Read a frame from the RealSense camera.
        
        Returns:
            Color frame as numpy array or None if failed
        """
        if self.pipeline is None:
            # Return mock data for testing
            return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        try:
            import pyrealsense2 as rs
            
            # Wait for frames
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            
            if color_frame:
                return np.asanyarray(color_frame.get_data())
            else:
                return None
                
        except Exception as e:
            print(f"[RealSenseSensor] Error reading frame: {e}")
            return None
    
    def release(self):
        """Release the RealSense resources."""
        if self.pipeline is not None:
            try:
                self.pipeline.stop()
                self.pipeline = None
                print("[RealSenseSensor] Released RealSense camera")
            except Exception as e:
                print(f"[RealSenseSensor] Error releasing camera: {e}")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.release() 