import math
from typing import Dict, List
from datetime import datetime

class MissionPlanner:
    """
    Mission Planning and Optimization
    Generates flight paths, calculates coverage, and optimizes routes
    """
    
    def __init__(self):
        self.missions = {}
        self.mission_counter = 0
    
    def generate_mission(self, name: str, center_lat: float, center_lon: float,
                        altitude: int, grid_spacing: int, speed: int = 10) -> Dict:
        """
        Generate a grid-based survey mission
        """
        self.mission_counter += 1
        mission_id = f"MISSION-{self.mission_counter:04d}"
        
        # Generate grid waypoints
        waypoints = self._generate_grid(center_lat, center_lon, grid_spacing)
        
        # Calculate coverage area
        area = len(waypoints) * (grid_spacing ** 2) / 10000  # in hectares
        
        # Calculate estimated time
        total_distance = self._calculate_distance(waypoints)
        estimated_time = (total_distance / speed) + 5  # Add 5 min for takeoff/land
        
        mission = {
            "id": mission_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "center_latitude": center_lat,
            "center_longitude": center_lon,
            "altitude": altitude,
            "waypoints": waypoints,
            "grid_spacing": grid_spacing,
            "speed": speed,
            "area_coverage": round(area, 2),
            "estimated_time": round(estimated_time, 1),
            "distance": round(total_distance, 2),
            "status": "planned"
        }
        
        self.missions[mission_id] = mission
        return mission
    
    def _generate_grid(self, center_lat: float, center_lon: float, 
                       spacing: int, size: int = 5) -> List[Dict]:
        """
        Generate grid waypoints for area coverage
        """
        waypoints = []
        
        # Convert spacing from meters to degrees (approximate)
        lat_offset = spacing / 111000  # 1 degree latitude ≈ 111 km
        lon_offset = spacing / (111000 * math.cos(math.radians(center_lat)))
        
        # Generate grid
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                lat = center_lat + (i * lat_offset)
                lon = center_lon + (j * lon_offset)
                waypoints.append({
                    "lat": round(lat, 6),
                    "lon": round(lon, 6),
                    "alt": 50  # 50m altitude
                })
        
        return waypoints
    
    def _calculate_distance(self, waypoints: List[Dict]) -> float:
        """
        Calculate total flight distance between waypoints
        """
        if len(waypoints) < 2:
            return 0
        
        total_distance = 0
        for i in range(len(waypoints) - 1):
            lat1 = math.radians(waypoints[i]['lat'])
            lon1 = math.radians(waypoints[i]['lon'])
            lat2 = math.radians(waypoints[i + 1]['lat'])
            lon2 = math.radians(waypoints[i + 1]['lon'])
            
            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.asin(math.sqrt(a))
            distance = 6371000 * c  # Earth radius in meters
            
            total_distance += distance
        
        return total_distance
    
    def optimize_route(self, mission_id: str) -> Dict:
        """
        Optimize flight path using nearest neighbor algorithm
        """
        if mission_id not in self.missions:
            raise Exception(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        waypoints = mission['waypoints']
        
        # Nearest neighbor optimization
        optimized = [waypoints[0]]
        remaining = set(range(1, len(waypoints)))
        
        while remaining:
            current = optimized[-1]
            nearest_idx = min(remaining, 
                            key=lambda i: self._point_distance(current, waypoints[i]))
            optimized.append(waypoints[nearest_idx])
            remaining.remove(nearest_idx)
        
        mission['waypoints'] = optimized
        mission['distance'] = round(self._calculate_distance(optimized), 2)
        mission['status'] = 'optimized'
        
        return mission
    
    def _point_distance(self, p1: Dict, p2: Dict) -> float:
        """
        Calculate distance between two points
        """
        lat1 = math.radians(p1['lat'])
        lon1 = math.radians(p1['lon'])
        lat2 = math.radians(p2['lat'])
        lon2 = math.radians(p2['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371000 * c
    
    def get_mission(self, mission_id: str) -> Dict:
        """
        Retrieve mission details
        """
        return self.missions.get(mission_id, None)
    
    def list_missions(self) -> List[Dict]:
        """
        List all missions
        """
        return list(self.missions.values())