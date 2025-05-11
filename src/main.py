import cv2
import numpy as np
from loguru import logger
from camera.realsense_camera import RealSenseCamera
from detection.pedestrian_detector import PedestrianDetector
from display.eye_animation import EyeAnimation
import matplotlib.pyplot as plt
import time

class DataVisualizer:
    """Manages the visualization of pedestrian data in separate windows."""
    
    def __init__(self):
        # Enable interactive mode for Matplotlib
        plt.ion()
        
        # Initialize window for pedestrian positions
        self.fig1, self.ax1 = plt.subplots(figsize=(6, 4))
        self.fig1.canvas.manager.set_window_title('Pedestrian Positions')
        self.ax1.set_title('Pedestrian Positions (X, Y)')
        self.ax1.set_xlabel('X-Position (Pixel)')
        self.ax1.set_ylabel('Y-Position (Pixel)')
        self.ax1.grid(True)
        self.ax1.set_xlim(0, 800)  # Image resolution
        self.ax1.set_ylim(0, 600)
        self.scatter = self.ax1.scatter([], [], c='blue', s=50)

        # Initialize window for pedestrian distances
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4))
        self.fig2.canvas.manager.set_window_title('Pedestrian Distances')
        self.ax2.set_title('Distances of Pedestrians')
        self.ax2.set_xlabel('Pedestrian ID')
        self.ax2.set_ylabel('Distance (m)')
        self.ax2.set_ylim(0, 5)  # Max distance from config
        self.bars = None

        # Initialize window for detection status
        self.fig3, self.ax3 = plt.subplots(figsize=(6, 4))
        self.fig3.canvas.manager.set_window_title('Detection Status')
        self.ax3.set_title('Number of Detected Pedestrians Over Time')
        self.ax3.set_xlabel('Time (s)')
        self.ax3.set_ylabel('Number of Pedestrians')
        self.ax3.set_ylim(0, 5)  # Max 4 pedestrians + buffer
        self.times = []
        self.counts = []
        self.line, = self.ax3.plot([], [], 'r-')

        # Initialize window for depth map
        self.fig4, self.ax4 = plt.subplots(figsize=(6, 4))
        self.fig4.canvas.manager.set_window_title('Depth Map')
        self.ax4.set_title('Depth Map with Pedestrian Bounding Boxes')
        self.ax4.set_xlabel('X (Pixel)')
        self.ax4.set_ylabel('Y (Pixel)')
        self.depth_im = None
        self.depth_cbar = None

        self.start_time = time.time()
        self.pedestrians = []
        self.bboxes = []
        
        # Flags to track window status
        self.windows_open = True

    def update_plots(self, pedestrians, bboxes, depth_image):
        """Updates the visualizations based on the current pedestrian data and depth image."""
        if not self.windows_open:
            return
        
        try:
            self.pedestrians = pedestrians
            self.bboxes = bboxes

            # Plot 1: Pedestrian positions
            if pedestrians:
                x = [p[0] for p in pedestrians]
                y = [p[1] for p in pedestrians]
                self.scatter.set_offsets(np.c_[x, y])
            else:
                self.scatter.set_offsets(np.empty((0, 2)))

            # Plot 2: Distances
            if self.bars:
                for bar in self.bars:
                    bar.remove()
            distances = [p[2] for p in pedestrians] if pedestrians else [0]
            self.bars = self.ax2.bar(range(len(distances)), distances, color='green')
            self.ax2.set_xlim(-0.5, max(3.5, len(distances) - 0.5))

            # Plot 3: Detection status
            current_time = time.time() - self.start_time
            self.times.append(current_time)
            self.counts.append(len(pedestrians))
            # Limit data to the last 30 seconds
            if self.times[-1] > 30:
                self.times = [t for t in self.times if t > self.times[-1] - 30]
                self.counts = self.counts[-len(self.times):]
            self.line.set_data(self.times, self.counts)
            self.ax3.set_xlim(max(0, self.times[-1] - 30), max(30, self.times[-1]))

            # Plot 4: Depth map
            if depth_image is not None:
                # Convert depth image to meters and clip to max distance (5m)
                depth_data = depth_image * 0.001  # Convert mm to meters
                depth_data = np.clip(depth_data, 0, 5)
                
                # Clear previous depth image
                if self.depth_im:
                    self.depth_im.remove()
                
                # Display depth image as heatmap
                self.depth_im = self.ax4.imshow(depth_data, cmap='viridis', vmin=0, vmax=5)
                
                # Add colorbar only once
                if self.depth_cbar is None:
                    self.depth_cbar = self.fig4.colorbar(self.depth_im, ax=self.ax4, label='Distance (m)')
                
                # Overlay bounding boxes
                for (x1, y1, x2, y2, _) in bboxes:
                    rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='red', facecolor='none')
                    self.ax4.add_patch(rect)
            
            # Draw the plots only if figures are still open
            if plt.fignum_exists(self.fig1.number):
                self.fig1.canvas.draw()
                self.fig1.canvas.flush_events()
            if plt.fignum_exists(self.fig2.number):
                self.fig2.canvas.draw()
                self.fig2.canvas.flush_events()
            if plt.fignum_exists(self.fig3.number):
                self.fig3.canvas.draw()
                self.fig3.canvas.flush_events()
            if plt.fignum_exists(self.fig4.number):
                self.fig4.canvas.draw()
                self.fig4.canvas.flush_events()

        except Exception as e:
            logger.error(f"Error updating plots: {e}")
            self.windows_open = False

    def close(self):
        """Closes all Matplotlib windows."""
        plt.close('all')
        self.windows_open = False

def main():
    """Main function to run the pedestrian communication system."""
    camera = None
    camera_started = False
    visualizer = None
    prev_time = time.time()  # Für FPS-Berechnung
    try:
        # Initialize components
        camera = RealSenseCamera('config/settings.yaml')
        detector = PedestrianDetector('config/settings.yaml')
        display = EyeAnimation('config/settings.yaml')
        visualizer = DataVisualizer()
        logger.info("All components initialized.")

        # Start the camera
        camera.start()
        camera_started = True

        # Create window for camera image
        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Camera', 800, 600)

        while True:
            # Read frames
            color_image, depth_image = camera.get_frames()
            if color_image is None or depth_image is None:
                logger.warning("No valid frames received. Skipping iteration.")
                continue

            # Berechne FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if curr_time != prev_time else 0
            prev_time = curr_time

            # Detect pedestrians
            pedestrians, bboxes = detector.detect(color_image, depth_image)

            # Draw bounding boxes and distances on the camera image
            for (x1, y1, x2, y2, distance) in bboxes:
                # Draw rectangle
                cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Draw "Distance: [distance]" at the corner
                text_distance = f"Distance: {distance:.2f}m"
                cv2.putText(
                    color_image, text_distance, (x1 + 0, y1 - 17),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )
                # Draw "Pedestrian" inside the bounding box
                text_pedestrian = "Pedestrian"
                cv2.putText(
                    color_image, text_pedestrian, (x1 + 0, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )

            # Füge FPS-Overlay hinzu
            try:
                text = f"FPS: {fps:.1f}"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(color_image, (0, 0), (text_width + 10, text_height + 10), (0, 0, 0), -1)
                cv2.putText(
                    color_image, text, (5, text_height + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
                )
            except Exception as e:
                logger.error(f"Fehler beim Hinzufügen des FPS-Overlays: {e}")

            # Show camera image
            cv2.imshow('Camera', color_image)

            # Update eye display
            display.show(pedestrians)

            # Update visualizations
            visualizer.update_plots(pedestrians, bboxes, depth_image)

            # Exit on 'q' key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("Programm durch Benutzer beendet ('q' gedrückt).")
                break

    except Exception as e:
        logger.error(f"Error in main program: {e}")
    finally:
        # Clean up resources
        if camera is not None and camera_started:
            camera.stop()
        if visualizer is not None:
            visualizer.close()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        logger.info("Program terminated.")

if __name__ == "__main__":
    main()