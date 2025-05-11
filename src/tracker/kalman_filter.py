import numpy as np
from filterpy.kalman import KalmanFilter
from loguru import logger

class KalmanBoxTracker:
    """Tracks bounding boxes of pedestrians using a Kalman Filter."""
    
    _count = 0

    def __init__(self, bbox: np.ndarray):
        """
        Initializes the tracker with a bounding box.
        
        Args:
            bbox: Array of shape [x1, y1, x2, y2].
        """
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        # State transition matrix
        self.kf.F = np.array([
            [1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ])
        # Measurement matrix
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ])
        # Measurement noise
        self.kf.R[2:, 2:] *= 10.
        # Prediction uncertainty
        self.kf.P[4:, 4:] *= 1000.
        self.kf.P *= 10.
        # Process noise
        self.kf.Q[-1, -1] *= 0.01
        self.kf.Q[4:, 4:] *= 0.01

        self.kf.x[:4] = np.reshape(bbox, (4, 1))
        self.time_since_update = 0
        self.id = KalmanBoxTracker._count
        KalmanBoxTracker._count += 1
        self.hit_streak = 0
        logger.debug(f"Tracker {self.id} initialized with bbox {bbox}")

    def update(self, bbox: np.ndarray):
        """Updates the tracker with a new bounding box."""
        self.time_since_update = 0
        self.hit_streak += 1
        self.kf.update(np.reshape(bbox, (4, 1)))
        logger.debug(f"Tracker {self.id} updated with bbox {bbox}")

    def predict(self) -> np.ndarray:
        """Performs a prediction and returns the new state."""
        self.time_since_update += 1
        self.kf.predict()
        return self.kf.x[:4].flatten()

    def get_state(self) -> np.ndarray:
        """Returns the current bounding box."""
        return self.kf.x[:4].flatten()