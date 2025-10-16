import cv2
import numpy as np

def draw_traffic_lights(frame, controller):
    """Draw traffic light states on the frame."""
    height, width = frame.shape[:2]
    margin = 50
    
    for i, light in controller.lights.items():
        # Calculate position for traffic light visualization
        x = margin if i < 2 else width - margin
        y = margin if i % 2 == 0 else height - margin
        
        # Draw traffic light
        color = {
            'RED': (0, 0, 255),
            'YELLOW': (0, 255, 255),
            'GREEN': (0, 255, 0)
        }[light.state.value]
        
        cv2.circle(frame, (x, y), 20, color, -1)
        cv2.putText(frame, f"Light {i}", (x-30, y-30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame

def annotate_frame(frame, detections, controller):
    """Add visualizations to the frame."""
    # Draw traffic lights
    frame = draw_traffic_lights(frame, controller)
    
    # Draw detection boxes
    for box in detections:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, "Ambulance", (x1, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Add emergency mode indicator
    if controller.emergency_mode:
        cv2.putText(frame, "EMERGENCY MODE", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return frame