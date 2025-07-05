"""
Webcam sensor interface with OpenCV support.
"""

import cv2
import numpy as np
from typing import Optional, Tuple

class WebcamSensor:
    """Webcam sensor using OpenCV."""
    
    def __init__(self, index: int = 0, resolution: Tuple[int, int] = (640, 480), fps: int = 30):
        """
        Initialize webcam sensor.
        
        Args:
            index: Camera device index
            resolution: Camera resolution (width, height)
            fps: Frames per second
        """
        self.index = index
        self.resolution = resolution
        self.fps = fps
        self.cap = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the camera capture."""
        try:
            self.cap = cv2.VideoCapture(self.index)
            
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open camera {self.index}")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            print(f"[WebcamSensor] Initialized camera {self.index} at {self.resolution[0]}x{self.resolution[1]} @ {self.fps}fps")
            
        except Exception as e:
            print(f"[WebcamSensor] Error initializing camera: {e}")
            self.cap = None
    
    def read(self) -> Optional[np.ndarray]:
        """
        Read a frame from the camera.
        
        Returns:
            Frame as numpy array or None if failed
        """
        if self.cap is None or not self.cap.isOpened():
            return None
        
        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                return None
        except Exception as e:
            print(f"[WebcamSensor] Error reading frame: {e}")
            return None
    
    def release(self):
        """Release the camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print(f"[WebcamSensor] Released camera {self.index}")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.release() 