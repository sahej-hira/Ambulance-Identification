import time
from enum import Enum

class LightState(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class TrafficLight:
    def __init__(self, id):
        self.id = id
        self.state = LightState.RED
        self.last_change = time.time()
    
    def set_state(self, state):
        self.state = state
        self.last_change = time.time()

class TrafficLightController:
    def __init__(self):
        """Initialize the traffic light controller."""
        self.lights = {}
        self.emergency_mode = False
        self.setup_traffic_lights()
    
    def setup_traffic_lights(self):
        """Setup the traffic light network."""
        # Example setup with 4 traffic lights at an intersection
        for i in range(4):
            self.lights[i] = TrafficLight(i)
    
    def prioritize_emergency(self):
        """Give priority to emergency vehicles."""
        if not self.emergency_mode:
            self.emergency_mode = True
            # Implementation of emergency traffic control logic
            # Set all lights to red except the ones in ambulance's path
            for light in self.lights.values():
                light.set_state(LightState.RED)
    
    def normal_operation(self):
        """Return to normal traffic light operation."""
        if self.emergency_mode:
            self.emergency_mode = False
            # Reset to normal traffic pattern
            self._update_normal_pattern()
    
    def _update_normal_pattern(self):
        """Update traffic lights according to normal pattern."""
        # Simple traffic pattern implementation
        current_time = time.time()
        cycle_duration = 30  # seconds
        
        for light in self.lights.values():
            time_in_cycle = (current_time - light.last_change) % cycle_duration
            
            if time_in_cycle < 20:
                light.set_state(LightState.GREEN)
            elif time_in_cycle < 25:
                light.set_state(LightState.YELLOW)
            else:
                light.set_state(LightState.RED)