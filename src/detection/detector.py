import cv2
import torch
from ultralytics import YOLO
import numpy as np

class AmbulanceDetector:
    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.25):
        """Initialize the ambulance detector with YOLO model."""
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        # Vehicle class IDs in COCO dataset: car=2, truck=7, bus=5
        self.vehicle_classes = [2, 5, 7]  # We'll detect these as potential emergency vehicles

    def process_frame(self, frame):
        """Process a single frame and detect potential ambulances/emergency vehicles."""
        results = self.model(frame, verbose=False)
        ambulances = []
        
        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Check if detection is a vehicle with sufficient confidence
                if cls_id in self.vehicle_classes and conf >= self.conf_threshold:
                    box_coords = box.xyxy[0].cpu().numpy()
                    ambulances.append({
                        'bbox': box_coords,
                        'confidence': conf,
                        'class': cls_id
                    })
        
        return ambulances

    def process_video(self, video_path, traffic_controller):
        """Process video stream and control traffic lights."""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return
        
        print("Processing video... Press 'q' to quit")
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every frame (you can skip frames for faster processing)
            if frame_count % 2 == 0:  # Process every 2nd frame
                # Detect vehicles/ambulances
                detections = self.process_frame(frame)
                
                # Update traffic lights based on detections
                # In real scenario, we'd have logic to identify actual ambulances
                # For demo, we treat any large vehicle as potential emergency vehicle
                if len(detections) > 0:
                    # Check if there are large vehicles (trucks/buses) that might be ambulances
                    large_vehicles = [d for d in detections if d['class'] in [5, 7]]  # bus or truck
                    if large_vehicles:
                        traffic_controller.prioritize_emergency()
                    else:
                        traffic_controller.normal_operation()
                else:
                    traffic_controller.normal_operation()
                
                # Visualize results
                for detection in detections:
                    box = detection['bbox']
                    x1, y1, x2, y2 = map(int, box)
                    conf = detection['confidence']
                    cls_id = detection['class']
                    
                    # Color based on vehicle type
                    color = (0, 255, 0) if cls_id in [5, 7] else (255, 0, 0)
                    label = f"Vehicle: {conf:.2f}"
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Add traffic light status
                status = "EMERGENCY MODE" if traffic_controller.emergency_mode else "NORMAL MODE"
                color = (0, 0, 255) if traffic_controller.emergency_mode else (0, 255, 0)
                cv2.putText(frame, status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Display frame
            cv2.imshow('Ambulance Detection System', frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"\nProcessed {frame_count} frames")