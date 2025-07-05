"""
Dataset sensor interface for TUM/KITTI datasets.
"""

import os
import numpy as np
from typing import Optional, Dict, List

class DatasetSensor:
    """Dataset sensor for reading TUM/KITTI datasets."""
    
    def __init__(self, path: str, dataset_type: str = 'TUM'):
        """
        Initialize dataset sensor.
        
        Args:
            path: Path to dataset directory
            dataset_type: Type of dataset ('TUM' or 'KITTI')
        """
        self.path = path
        self.dataset_type = dataset_type
        self.image_files = []
        self.current_index = 0
        self._initialize()
    
    def _initialize(self):
        """Initialize the dataset reader."""
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"Dataset path not found: {self.path}")
            
            if self.dataset_type == 'TUM':
                self._load_tum_dataset()
            elif self.dataset_type == 'KITTI':
                self._load_kitti_dataset()
            else:
                raise ValueError(f"Unsupported dataset type: {self.dataset_type}")
                
            print(f"[DatasetSensor] Loaded {len(self.image_files)} images from {self.dataset_type} dataset")
            
        except Exception as e:
            print(f"[DatasetSensor] Error initializing dataset: {e}")
            self.image_files = []
    
    def _load_tum_dataset(self):
        """Load TUM dataset structure."""
        # Look for image files in common TUM dataset structure
        image_extensions = ['.png', '.jpg', '.jpeg']
        
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    self.image_files.append(os.path.join(root, file))
        
        self.image_files.sort()
    
    def _load_kitti_dataset(self):
        """Load KITTI dataset structure."""
        # Look for image files in common KITTI dataset structure
        image_dir = os.path.join(self.path, 'image_2')
        if os.path.exists(image_dir):
            image_extensions = ['.png', '.jpg', '.jpeg']
            
            for file in os.listdir(image_dir):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    self.image_files.append(os.path.join(image_dir, file))
        
        self.image_files.sort()
    
    def read(self) -> Optional[np.ndarray]:
        """
        Read the next frame from the dataset.
        
        Returns:
            Frame as numpy array or None if end of dataset
        """
        if self.current_index >= len(self.image_files):
            return None
        
        try:
            import cv2
            image_path = self.image_files[self.current_index]
            frame = cv2.imread(image_path)
            self.current_index += 1
            return frame
            
        except Exception as e:
            print(f"[DatasetSensor] Error reading frame {self.current_index}: {e}")
            self.current_index += 1
            return None
    
    def reset(self):
        """Reset to the beginning of the dataset."""
        self.current_index = 0
    
    def release(self):
        """Release dataset resources."""
        self.image_files = []
        self.current_index = 0
        print("[DatasetSensor] Released dataset")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.release() 