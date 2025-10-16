import argparse
from detection.detector import AmbulanceDetector
from simulation.traffic_controller import TrafficLightController

def parse_args():
    parser = argparse.ArgumentParser(description='Ambulance Detection and Traffic Control System')
    parser.add_argument('--input', type=str, help='Path to input video file')
    parser.add_argument('--model', type=str, default='yolov8n.pt', help='Path to YOLO model')
    parser.add_argument('--conf', type=float, default=0.25, help='Confidence threshold')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Initialize detector and controller
    detector = AmbulanceDetector(model_path=args.model, conf_threshold=args.conf)
    controller = TrafficLightController()
    
    # Start processing
    detector.process_video(args.input, controller)

if __name__ == '__main__':
    main()