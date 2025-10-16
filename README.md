# Ambulance Detection and Traffic Light Control System

This project implements a machine learning-based system for detecting ambulances in traffic and automatically controlling traffic lights to give priority to emergency vehicles.

## Features

- Real-time ambulance detection using YOLOv8
- Automated traffic light control system
- Traffic flow simulation
- Support for video input processing

## Project Structure

```
UrgencyAmbulance/
├── src/
│   ├── detection/      # ML model and video processing
│   ├── simulation/     # Traffic light control logic
│   └── utils/          # Helper functions
├── data/               # Sample data and videos
├── models/             # Trained models
├── tests/              # Unit tests
└── requirements.txt    # Project dependencies
```

## Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the pre-trained YOLO model (will be downloaded automatically on first run)

## Usage

1. Run the main detection script:
```bash
python src/main.py --input <video_path>
```

2. For simulation mode:
```bash
python src/simulation/simulate.py
```

## Development

- To run tests:
```bash
pytest tests/
```

- To train on custom data:
```bash
python src/detection/train.py --data <data_config.yaml>
```

## License

MIT License