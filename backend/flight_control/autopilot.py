import time
import random
from datetime import datetime
from typing import Dict, List, Optional

class Autopilot:
    """
    UAV Autopilot Control System
    Manages drone flight control, navigation, and telemetry
    """
    
    def __init__(self):
        self.drone_id = "DRONE-001"
        self.is_armed = False
        self.is_flying = False
        self.battery = 100
        self.altitude = 0
        self.latitude = 9.0320  # Addis Ababa default
        self.longitude = 38.7469
        self.heading = 0
        self.speed = 0
        self.telemetry_history = []
        self.waypoints = []
        self.current_waypoint = 0
        
    def arm(self) -> Dict:
        """
        Arm the drone for takeoff
        """
        if self.battery < 20:
            raise Exception("Battery too low to arm")
        self.is_armed = True
        return {"status": "armed", "message": "Drone ready for flight"}
    
    def disarm(self) -> Dict:
        """
        Disarm the drone
        """
        self.is_armed = False
        self.is_flying = False
        self.speed = 0
        return {"status": "disarmed", "message": "Drone disarmed"}
    
    def takeoff(self, target_altitude: int) -> Dict:
        """
        Takeoff to target altitude
        """
        if not self.is_armed:
            raise Exception("Drone must be armed before takeoff")
        
        self.is_flying = True
        self.altitude = 0
        
        # Simulate climb
        while self.altitude < target_altitude:
            self.altitude += 1
            self.battery -= 0.1
            time.sleep(0.01)  # Simulate time
        
        return {
            "status": "airborne",
            "altitude": self.altitude,
            "battery": self.battery
        }
    
    def goto_waypoint(self, latitude: float, longitude: float, altitude: int) -> Dict:
        """
        Navigate to a waypoint
        """
        if not self.is_flying:
            raise Exception("Drone must be flying")
        
        # Calculate distance (simplified)
        distance = abs(self.latitude - latitude) + abs(self.longitude - longitude)
        
        # Simulate flight
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.battery -= distance * 0.5
        
        return {
            "status": "waypoint_reached",
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude
        }
    
    def set_heading(self, heading: int) -> Dict:
        """
        Set drone heading (0-360 degrees)
        """
        self.heading = heading % 360
        return {"heading": self.heading}
    
    def set_speed(self, speed: float) -> Dict:
        """
        Set drone speed (m/s)
        """
        if speed > 20:
            speed = 20  # Max speed
        self.speed = speed
        return {"speed": self.speed}
    
    def return_to_launch(self) -> Dict:
        """
        Return to home position and land
        """
        if not self.is_flying:
            return {"status": "not_flying"}
        
        # Simulate RTL
        self.latitude = 9.0320
        self.longitude = 38.7469
        self.altitude = 0
        self.is_flying = False
        self.battery -= 5
        
        return {"status": "landed", "message": "Returned to launch"}
    
    def land(self) -> Dict:
        """
        Land the drone at current location
        """
        while self.altitude > 0:
            self.altitude -= 1
            self.battery -= 0.05
            time.sleep(0.01)
        
        self.is_flying = False
        self.speed = 0
        return {"status": "landed", "altitude": self.altitude}
    
    def execute_mission(self, mission_id: str) -> Dict:
        """
        Execute a full mission from waypoints
        """
        try:
            # Arm and takeoff
            self.arm()
            self.takeoff(50)  # 50m altitude
            
            # Execute waypoints
            for i, wp in enumerate(self.waypoints):
                if self.battery < 15:
                    self.return_to_launch()
                    break
                
                self.goto_waypoint(wp['lat'], wp['lon'], wp['alt'])
                self.current_waypoint = i + 1
                time.sleep(1)  # Simulate mission time
            
            # Return and land
            self.return_to_launch()
            self.disarm()
            
            return {
                "status": "mission_complete",
                "mission_id": mission_id,
                "battery": self.battery
            }
        except Exception as e:
            self.return_to_launch()
            self.disarm()
            return {"status": "mission_failed", "error": str(e)}
    
    def get_status(self) -> Dict:
        """
        Get current drone status
        """
        # Simulate battery drain
        if self.is_flying:
            self.battery -= random.uniform(0.1, 0.5)
        
        return {
            "drone_id": self.drone_id,
            "armed": self.is_armed,
            "flying": self.is_flying,
            "battery": round(self.battery, 1),
            "altitude": round(self.altitude, 1),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "heading": self.heading,
            "speed": round(self.speed, 2),
            "timestamp": datetime.now().isoformat(),
            "current_waypoint": self.current_waypoint,
            "total_waypoints": len(self.waypoints)
        }
    
    def load_waypoints(self, waypoints: List[Dict]):
        """
        Load mission waypoints
        """
        self.waypoints = waypoints
        self.current_waypoint = 0
        return {"waypoints_loaded": len(waypoints)}