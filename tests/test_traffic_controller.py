import pytest
from src.simulation.traffic_controller import TrafficLightController, LightState

def test_traffic_light_initialization():
    controller = TrafficLightController()
    assert len(controller.lights) == 4
    assert not controller.emergency_mode
    
    for light in controller.lights.values():
        assert light.state == LightState.RED

def test_emergency_mode():
    controller = TrafficLightController()
    controller.prioritize_emergency()
    
    assert controller.emergency_mode
    for light in controller.lights.values():
        assert light.state == LightState.RED
        
def test_normal_operation():
    controller = TrafficLightController()
    controller.emergency_mode = True
    controller.normal_operation()
    
    assert not controller.emergency_mode