import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipeline.start(config)
try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        center_x, center_y = 640, 360
        depth_roi = depth_image[center_y-50:center_y+50, center_x-50:center_x+50]
        valid_depth = depth_roi[depth_roi > 0]
        if len(valid_depth) > 0:
            distance = np.median(valid_depth) * 0.001
            print(f"Entfernung im Zentrum: {distance:.3f}m")
        cv2.imshow('Color', color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()