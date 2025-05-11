from ultralytics import YOLO
import numpy as np
import yaml
from tracker.kalman_filter import KalmanBoxTracker
from loguru import logger

class PedestrianDetector:
    """Detects and tracks pedestrians using YOLOv8 and Kalman Filter."""
    
    def __init__(self, config_path: str):
        """Initializes the detector with configuration parameters."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.model_name = config['detection']['model']
                self.confidence = config['detection']['confidence']
                self.max_distance = config['camera']['depth_threshold']
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
        
        self.model = YOLO(self.model_name)
        self.trackers = []
        logger.info(f"YOLOv8 model {self.model_name} loaded.")

    def detect(self, color_image: np.ndarray, depth_image: np.ndarray) -> tuple[list, list]:
        """
        Detects pedestrians and tracks them with Kalman Filters.
        
        Args:
            color_image: Color image from the camera.
            depth_image: Depth image from the camera.
        
        Returns:
            Tuple (pedestrians, bboxes):
                - pedestrians: List of tuples (center_x, center_y, distance) for up to 4 pedestrians.
                - bboxes: List of tuples (x1, y1, x2, y2, distance) for bounding boxes.
        """
        try:
            # Ensure color_image is contiguous
            color_image = np.ascontiguousarray(color_image)
            # YOLOv8 detection
            results = self.model.predict(source=color_image, classes=[0], conf=self.confidence, verbose=False)
            detections = []
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].numpy()
                    detections.append(np.array([x1, y1, x2, y2]))
            logger.debug(f"{len(detections)} YOLOv8 detections.")

            # Update or create trackers
            new_trackers = []
            bboxes = []
            for det in detections[:4]:  # Limit to 4 pedestrians
                # Calculate distance
                x1, y1, x2, y2 = map(int, det)
                depth_roi = depth_image[y1:y2, x1:x2]
                valid_depth = depth_roi[depth_roi > 0]
                if len(valid_depth) == 0:
                    logger.warning(f"No valid depth values for BBox [{x1}, {y1}, {x2}, {y2}].")
                    continue
                distance = np.mean(valid_depth) * 0.001  # In meters
                logger.debug(f"Distance for BBox [{x1}, {y1}, {x2}, {y2}]: {distance:.2f} m")
                if distance > self.max_distance:
                    logger.debug(f"Pedestrian at {distance:.2f} m ignored (max: {self.max_distance} m).")
                    continue

                # Store bounding box for visualization
                bboxes.append((x1, y1, x2, y2, distance))

                # Find the best tracker or create a new one
                best_tracker = None
                min_dist = float('inf')
                for tracker in self.trackers:
                    pred = tracker.predict()
                    dist = np.linalg.norm(pred - det)
                    if dist < min_dist:
                        min_dist = dist
                        best_tracker = tracker
                
                if min_dist < 50:  # Threshold for assignment
                    best_tracker.update(det)
                    new_trackers.append(best_tracker)
                else:
                    new_trackers.append(KalmanBoxTracker(det))
            
            self.trackers = new_trackers

            # Collect positions
            pedestrians = []
            for tracker in self.trackers[:4]:
                bbox = tracker.get_state()
                x1, y1, x2, y2 = map(int, bbox)
                depth_roi = depth_image[y1:y2, x1:x2]
                valid_depth = depth_roi[depth_roi > 0]
                if len(valid_depth) == 0:
                    logger.warning(f"No valid depth values for tracked BBox [{x1}, {y1}, {x2}, {y2}].")
                    continue
                distance = np.mean(valid_depth) * 0.001
                if distance > self.max_distance:
                    logger.debug(f"Tracked pedestrian at {distance:.2f} m ignored.")
                    continue
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                pedestrians.append((center_x, center_y, distance))
            
            logger.debug(f"{len(pedestrians)} pedestrians detected after depth filtering.")
            return pedestrians, bboxes
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return [], []