"""
FastSLAM algorithm implementation.
"""

import numpy as np
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class SLAMResult:
    """Result from SLAM processing."""
    pose: Optional[np.ndarray] = None
    map: Optional[np.ndarray] = None
    particles: Optional[List[np.ndarray]] = None
    tracking_status: str = "OK"

class FastSLAM:
    """FastSLAM algorithm implementation using particle filter."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize FastSLAM.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.num_particles = self.config.get('num_particles', 100)
        self.particles = []
        self.weights = []
        self.landmarks = []
        self.frame_count = 0
        self._initialize()
    
    def _initialize(self):
        """Initialize particle filter."""
        try:
            # Initialize particles with random poses
            for i in range(self.num_particles):
                # Random initial pose [x, y, theta]
                pose = np.random.randn(3) * 0.1
                self.particles.append(pose)
                self.weights.append(1.0 / self.num_particles)
            
            print(f"[FastSLAM] Initialized {self.num_particles} particles")
            
        except Exception as e:
            print(f"[FastSLAM] Error initializing: {e}")
    
    def process(self, frame: np.ndarray) -> Optional[SLAMResult]:
        """
        Process a frame with FastSLAM.
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            SLAMResult with pose, map, and particles
        """
        if frame is None:
            return None
        
        try:
            # Simulate motion model (predict step)
            self._predict()
            
            # Simulate measurement model (update step)
            self._update(frame)
            
            # Resample particles
            self._resample()
            
            # Get best particle as current pose
            best_particle_idx = np.argmax(self.weights)
            current_pose = self.particles[best_particle_idx]
            
            # Create mock landmarks
            landmarks = np.random.randn(50, 2) * 10  # 2D landmarks
            
            # Create result
            result = SLAMResult(
                pose=np.array([current_pose[0], current_pose[1], 0, 1]),  # Convert to 4D pose
                map=landmarks,
                particles=self.particles.copy(),
                tracking_status="OK"
            )
            
            self.frame_count += 1
            return result
            
        except Exception as e:
            print(f"[FastSLAM] Error processing frame: {e}")
            return SLAMResult(tracking_status="ERROR")
    
    def _predict(self):
        """Predict step: move particles according to motion model."""
        for i in range(self.num_particles):
            # Simple motion model: move forward with some noise
            motion = np.array([0.1, 0, 0])  # Forward motion
            noise = np.random.randn(3) * 0.01  # Motion noise
            
            self.particles[i] += motion + noise
    
    def _update(self, frame: np.ndarray):
        """Update step: update particle weights based on measurements."""
        # Simulate feature detection
        num_features = min(20, frame.shape[0] // 10)  # Mock feature count
        
        for i in range(self.num_particles):
            # Simple likelihood model
            # In real implementation, this would compare predicted vs actual measurements
            likelihood = np.exp(-0.1 * np.random.rand())  # Mock likelihood
            self.weights[i] *= likelihood
        
        # Normalize weights
        total_weight = sum(self.weights)
        if total_weight > 0:
            self.weights = [w / total_weight for w in self.weights]
    
    def _resample(self):
        """Resample particles based on weights."""
        # Systematic resampling
        new_particles = []
        new_weights = []
        
        # Calculate cumulative weights
        cumsum = np.cumsum(self.weights)
        
        # Resample
        for i in range(self.num_particles):
            u = np.random.uniform(0, 1)
            idx = np.searchsorted(cumsum, u)
            new_particles.append(self.particles[idx].copy())
            new_weights.append(1.0 / self.num_particles)
        
        self.particles = new_particles
        self.weights = new_weights
    
    def reset(self):
        """Reset the SLAM system."""
        self.particles = []
        self.weights = []
        self.landmarks = []
        self.frame_count = 0
        self._initialize()
        print("[FastSLAM] Reset SLAM system") 