import pyrealsense2 as rs
import numpy as np
import yaml
from loguru import logger

class RealSenseCamera:
    """Controls the Intel RealSense D456C camera for color and depth images."""
    
    def __init__(self, config_path: str):
        """Initializes the camera with configuration parameters."""
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)['camera']
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
        
        self.pipeline = rs.pipeline()
        self.config_rs = rs.config()
        self.config_rs.enable_stream(
            rs.stream.color,
            self.config['resolution'][0],
            self.config['resolution'][1],
            rs.format.bgr8,
            self.config['fps']
        )
        self.config_rs.enable_stream(
            rs.stream.depth,
            self.config['resolution'][0],
            self.config['resolution'][1],
            rs.format.z16,
            self.config['fps']
        )
        self.align = rs.align(rs.stream.color)
        logger.info("Camera initialized.")

    def check_camera_status(self) -> bool:
        """Checks if the camera is connected and available."""
        try:
            ctx = rs.context()
            devices = ctx.query_devices()
            if not devices:
                logger.error("No RealSense camera found.")
                return False
            logger.info(f"Camera found: {devices[0].get_info(rs.camera_info.name)}")
            return True
        except Exception as e:
            logger.error(f"Error checking camera status: {e}")
            return False

    def start(self):
        """Starts the camera stream."""
        if not self.check_camera_status():
            raise RuntimeError("Camera not available.")
        try:
            self.pipeline.start(self.config_rs)
            logger.info("Camera stream started.")
        except Exception as e:
            logger.error(f"Error starting the camera: {e}")
            raise

    def get_frames(self) -> tuple[np.ndarray, np.ndarray]:
        """Reads color and depth images."""
        try:
            frames = self.pipeline.wait_for_frames(timeout_ms=5000)
            aligned_frames = self.align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            if not color_frame or not depth_frame:
                logger.warning("Invalid frames received.")
                return None, None
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            logger.debug(f"Frames received: Color image {color_image.shape}, Depth image {depth_image.shape}")
            if np.all(depth_image == 0):
                logger.warning("Depth image contains only zeros.")
            return color_image, depth_image
        except Exception as e:
            logger.error(f"Error retrieving frames: {e}")
            return None, None

    def stop(self):
        """Stops the camera stream."""
        try:
            self.pipeline.stop()
            logger.info("Camera stream stopped.")
        except Exception as e:
            logger.error(f"Error stopping the camera: {e}")