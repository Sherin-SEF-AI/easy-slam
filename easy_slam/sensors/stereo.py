"""
Stereo camera sensor interface.
"""

import numpy as np
from typing import Optional, Tuple, Dict

class StereoSensor:
    """Stereo camera sensor."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize stereo sensor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.left_camera = None
        self.right_camera = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the stereo cameras."""
        try:
            # For now, use mock stereo cameras
            # In a real implementation, this would initialize two physical cameras
            print("[StereoSensor] Initialized stereo cameras (mock)")
            
        except Exception as e:
            print(f"[StereoSensor] Error initializing stereo cameras: {e}")
    
    def read(self) -> Optional[np.ndarray]:
        """
        Read a frame from the stereo cameras.
        
        Returns:
            Left frame as numpy array or None if failed
        """
        try:
            # Return mock stereo data for testing
            # In a real implementation, this would read from both cameras
            left_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            right_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # For now, return left frame only
            return left_frame
            
        except Exception as e:
            print(f"[StereoSensor] Error reading frame: {e}")
            return None
    
    def read_stereo(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Read both left and right frames.
        
        Returns:
            Tuple of (left_frame, right_frame) or (None, None) if failed
        """
        try:
            left_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            right_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            return left_frame, right_frame
            
        except Exception as e:
            print(f"[StereoSensor] Error reading stereo frames: {e}")
            return None, None
    
    def release(self):
        """Release the stereo camera resources."""
        try:
            if self.left_camera:
                self.left_camera.release()
            if self.right_camera:
                self.right_camera.release()
            print("[StereoSensor] Released stereo cameras")
        except Exception as e:
            print(f"[StereoSensor] Error releasing cameras: {e}")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.release() 