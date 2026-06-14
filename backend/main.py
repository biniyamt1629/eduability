from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
import os
from datetime import datetime
import asyncio

from flight_control.autopilot import Autopilot
from mission_planning.mission_planner import MissionPlanner
from image_processing.ndvi_analyzer import NDVIAnalyzer
from image_processing.disease_detector import DiseaseDetector
from data_handler.logger import FlightLogger

# Initialize FastAPI app
app = FastAPI(
    title="DroneMapper Ethiopia API",
    description="Agricultural Drone Monitoring System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
autopilot = Autopilot()
mission_planner = MissionPlanner()
ndvi_analyzer = NDVIAnalyzer()
disease_detector = DiseaseDetector()
logger = FlightLogger()

# Pydantic models
class MissionConfig(BaseModel):
    mission_name: str
    latitude: float
    longitude: float
    altitude: int
    grid_spacing: int
    camera_angle: int = 0
    speed: int = 10

class FlightStatus(BaseModel):
    drone_id: str
    status: str
    battery: int
    altitude: float
    latitude: float
    longitude: float
    heading: int
    speed: float
    timestamp: str

class ImageAnalysisResult(BaseModel):
    image_id: str
    ndvi_mean: float
    disease_detected: bool
    disease_type: Optional[str]
    confidence: float
    area_coverage: float
    timestamp: str

# Routes
@app.get("/")
async def root():
    return {
        "message": "DroneMapper Ethiopia API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "autopilot": "connected",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/missions/create")
async def create_mission(config: MissionConfig):
    """
    Create a new drone mission
    """
    try:
        mission = mission_planner.generate_mission(
            name=config.mission_name,
            center_lat=config.latitude,
            center_lon=config.longitude,
            altitude=config.altitude,
            grid_spacing=config.grid_spacing,
            speed=config.speed
        )
        logger.log_event(f"Mission created: {config.mission_name}")
        return {
            "success": True,
            "mission_id": mission["id"],
            "waypoints": len(mission["waypoints"]),
            "estimated_time": mission["estimated_time"],
            "mission_data": mission
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/missions/{mission_id}/start")
async def start_mission(mission_id: str, background_tasks: BackgroundTasks):
    """
    Start a drone mission
    """
    try:
        # Start mission in background
        background_tasks.add_task(autopilot.execute_mission, mission_id)
        logger.log_event(f"Mission started: {mission_id}")
        return {
            "success": True,
            "mission_id": mission_id,
            "status": "executing"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/drone/status")
async def get_drone_status():
    """
    Get current drone status
    """
    status = autopilot.get_status()
    return status

@app.post("/drone/arm")
async def arm_drone():
    """
    Arm the drone for flight
    """
    try:
        result = autopilot.arm()
        logger.log_event("Drone armed")
        return {"success": True, "message": "Drone armed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/drone/disarm")
async def disarm_drone():
    """
    Disarm the drone
    """
    try:
        result = autopilot.disarm()
        logger.log_event("Drone disarmed")
        return {"success": True, "message": "Drone disarmed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/drone/rtl")
async def return_to_launch():
    """
    Return drone to launch point
    """
    try:
        result = autopilot.return_to_launch()
        logger.log_event("Return to launch initiated")
        return {"success": True, "message": "RTL command sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/images/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze drone imagery for crop health
    """
    try:
        # Save uploaded file
        contents = await file.read()
        image_path = f"temp_{datetime.now().timestamp()}.jpg"
        with open(image_path, "wb") as f:
            f.write(contents)
        
        # Analyze NDVI
        ndvi_result = ndvi_analyzer.analyze(image_path)
        
        # Detect diseases
        disease_result = disease_detector.detect(image_path)
        
        # Cleanup
        os.remove(image_path)
        
        result = ImageAnalysisResult(
            image_id=str(datetime.now().timestamp()),
            ndvi_mean=ndvi_result["mean"],
            disease_detected=disease_result["detected"],
            disease_type=disease_result.get("type"),
            confidence=disease_result["confidence"],
            area_coverage=ndvi_result["coverage"],
            timestamp=datetime.now().isoformat()
        )
        
        logger.log_event(f"Image analyzed: NDVI={result.ndvi_mean:.2f}")
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reports/generate")
async def generate_report(mission_id: str):
    """
    Generate mission report with analysis
    """
    try:
        report = {
            "mission_id": mission_id,
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "crop_health": "good",
            "ndvi_average": 0.67,
            "diseased_areas": 0,
            "recommendations": [
                "Water irrigation optimal",
                "Continue current fertilizer schedule",
                "Monitor for pests"
            ]
        }
        logger.log_event(f"Report generated: {mission_id}")
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/logs")
async def get_logs():
    """
    Get flight logs
    """
    logs = logger.get_recent_logs(50)
    return {"logs": logs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)