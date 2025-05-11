import cv2
import numpy as np
import yaml
from utils.coordinate_utils import pixel_to_eye_space
from loguru import logger

class EyeAnimation:
    """Displays animated eyes based on pedestrian positions."""
    
    def __init__(self, config_path: str):
        """Initializes the eye display with configuration parameters."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)['display']
                self.window_size = config['window_size']
                self.eye_radius = config['eye_radius']
                self.pupil_radius = config['pupil_radius']
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
        
        self.signal_red = (0, 0, 255)
        self.signal_green = (0, 255, 0)
        self.eye_color = (255, 255, 255)
        self.background_gray = (128, 128, 128)  # Gray background color
        self.left_eye_center = (self.window_size[0] // 4, self.window_size[1] // 2)
        self.right_eye_center = (3 * self.window_size[0] // 4, self.window_size[1] // 2)
        cv2.namedWindow('Eyes', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Eyes', self.window_size[0], self.window_size[1])
        logger.info("Eye display initialized.")  # Was: "Augenanzeige initialisiert."

    def show(self, pedestrians: list):
        """
        Displays the eyes based on pedestrian positions.
        
        Args:
            pedestrians: List of tuples (center_x, center_y, distance).
        """
        try:
            image = np.zeros((self.window_size[1], self.window_size[0], 3), dtype=np.uint8)
            bg_color = self.background_gray  # Fixed gray background
            image[:] = bg_color
            logger.debug("Background color: Gray")  # Was: "Hintergrundfarbe: Grau"

            # Set pupil color based on pedestrian detection
            pupil_color = self.signal_green if pedestrians else self.signal_red
            logger.debug(f"Pupil color: {'Green' if pedestrians else 'Red'}")  # Was: "Pupillenfarbe: {'Grün' if pedestrians else 'Rot'}"

            # Draw eyes
            cv2.circle(image, self.left_eye_center, self.eye_radius, self.eye_color, -1)
            cv2.circle(image, self.right_eye_center, self.eye_radius, self.eye_color, -1)

            # Default pupil position
            pupil_left = self.left_eye_center
            pupil_right = self.right_eye_center

            if pedestrians:
                # Select the closest pedestrian
                closest_ped = min(pedestrians, key=lambda p: p[2])
                center_x, center_y, distance = closest_ped
                logger.debug(f"Closest pedestrian at x={center_x}, y={center_y}, distance={distance:.2f} m")  # Was: "Nächster Fußgänger bei x={center_x}, y={center_y}, Entfernung={distance:.2f} m"

                # Transform image coordinates to eye space
                left_eye_target = pixel_to_eye_space(
                    center_x, center_y, distance, self.left_eye_center, self.eye_radius
                )
                right_eye_target = pixel_to_eye_space(
                    center_x, center_y, distance, self.right_eye_center, self.eye_radius
                )
                logger.debug(f"Pupil positions: Left={left_eye_target}, Right={right_eye_target}")  # Was: "Pupillenpositionen: Links={left_eye_target}, Rechts={right_eye_target}"

                # Limit pupil movement within the eyes
                pupil_left = (
                    int(max(self.left_eye_center[0] - self.eye_radius + self.pupil_radius,
                            min(self.left_eye_center[0] + self.eye_radius - self.pupil_radius, left_eye_target[0]))),
                    int(max(self.left_eye_center[1] - self.eye_radius + self.pupil_radius,
                            min(self.left_eye_center[1] + self.eye_radius - self.pupil_radius, left_eye_target[1])))
                )
                pupil_right = (
                    int(max(self.right_eye_center[0] - self.eye_radius + self.pupil_radius,
                            min(self.right_eye_center[0] + self.eye_radius - self.pupil_radius, right_eye_target[0]))),
                    int(max(self.right_eye_center[1] - self.eye_radius + self.pupil_radius,
                            min(self.right_eye_center[1] + self.eye_radius - self.pupil_radius, right_eye_target[1])))
                )

            # Draw pupils
            cv2.circle(image, pupil_left, self.pupil_radius, pupil_color, -1)
            cv2.circle(image, pupil_right, self.pupil_radius, pupil_color, -1)

            cv2.imshow('Eyes', image)
            logger.debug("Eye display updated.")  # Was: "Augenanzeige aktualisiert."
        except Exception as e:
            logger.error(f"Error displaying eyes: {e}")  # Was: "Fehler bei der Anzeige der Augen: {e}"

    def __del__(self):
        """Closes the display window."""
        cv2.destroyAllWindows()