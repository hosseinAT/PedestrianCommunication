import numpy as np
from loguru import logger

def pixel_to_eye_space(pixel_x: int, pixel_y: int, distance: float, eye_center: tuple, eye_radius: int) -> tuple:
    """
    Transforms image coordinates into eye space coordinates for pupil movement.
    
    Args:
        pixel_x: X-coordinate of the pedestrian in the camera image.
        pixel_y: Y-coordinate of the pedestrian in the camera image.
        distance: Distance of the pedestrian in meters.
        eye_center: Center of the eye (x, y).
        eye_radius: Radius of the eye in pixels.
    
    Returns:
        Tuple (x, y) of the target pupil position in eye space.
    """
    try:
        # Assume image resolution (hardcoded for simplicity, ideally from config)
        image_width, image_height = 800, 600

        # Normalize image coordinates to the interval [-1, 1]
        norm_x = (pixel_x - image_width / 2) / (image_width / 2)
        norm_y = (pixel_y - image_height / 2) / (image_height / 2)

        # Scale movement based on distance
        # Closer pedestrians -> stronger movement; farther -> weaker movement
        max_distance = 2.0  # Corresponds to depth_threshold in settings.yaml
        scale = max(0.1, min(1.0, max_distance / max(1e-6, distance)))

        # Calculate relative pupil displacement in eye space
        pupil_offset_x = norm_x * eye_radius * scale
        pupil_offset_y = norm_y * eye_radius * scale

        # Calculate absolute pupil position
        pupil_x = eye_center[0] + pupil_offset_x
        pupil_y = eye_center[1] + pupil_offset_y

        logger.debug(f"Pixel ({pixel_x}, {pixel_y}) -> Pupil ({pupil_x:.2f}, {pupil_y:.2f}), "
                     f"Distance={distance:.2f}m, Scale={scale:.2f}")  # Was: "Entfernung=..., Skalierung=..."

        return (pupil_x, pupil_y)
    except Exception as e:
        logger.error(f"Error in coordinate transformation: {e}")  # Was: "Fehler bei der Koordinatentransformation: {e}"
        return eye_center  # Fallback: Pupil remains centered