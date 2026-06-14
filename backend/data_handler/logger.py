from datetime import datetime
from typing import List, Dict
import json

class FlightLogger:
    """
    Flight event logging system
    Tracks all mission activities and telemetry
    """
    
    def __init__(self):
        self.logs = []
        self.max_logs = 10000
    
    def log_event(self, message: str, level: str = "INFO", data: dict = None):
        """
        Log an event
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        self.logs.append(log_entry)
        
        # Keep only recent logs
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
        
        # Print to console
        print(f"[{log_entry['timestamp']}] {level}: {message}")
    
    def get_recent_logs(self, count: int = 50) -> List[Dict]:
        """
        Get recent log entries
        """
        return self.logs[-count:]
    
    def get_logs_by_level(self, level: str) -> List[Dict]:
        """
        Get logs filtered by level
        """
        return [log for log in self.logs if log['level'] == level]
    
    def export_logs(self, filename: str = "flight_logs.json"):
        """
        Export logs to JSON file
        """
        with open(filename, 'w') as f:
            json.dump(self.logs, f, indent=2)
        return filename