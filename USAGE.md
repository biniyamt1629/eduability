# DroneMapper Ethiopia - User Guide

## 🎯 Getting Started

### Step 1: Start the System

**Using Docker:**
```bash
docker-compose up -d
```

**Or manually:**
```bash
# Terminal 1: Start backend
python backend/main.py

# Terminal 2: Open frontend
python -m http.server 3000 --directory frontend
```

### Step 2: Access Dashboard
Open http://localhost:3000 in your web browser

## 🎮 Dashboard Overview

### Sections:

1. **Header**: System status and connection info
2. **Quick Stats**: Battery, altitude, NDVI, active missions
3. **Drone Controls**: Arm/disarm, RTL, manual control
4. **Status Panel**: Real-time drone telemetry
5. **Mission Map**: Interactive map with waypoints
6. **Crop Analysis**: NDVI score, disease detection, recommendations
7. **Charts**: Battery and altitude trends

## 🚁 Operating the Drone

### Basic Operations

#### 1. Arm the Drone
- Click **"✓ Arm Drone"** button
- Wait for confirmation
- Battery must be > 20%

#### 2. Create a Mission
- Fill in mission parameters:
  - **Mission Name**: e.g., "Farm Survey 2026-06-14"
  - **Latitude/Longitude**: Center of survey area
  - **Altitude**: 50m (default, can adjust)
  - **Grid Spacing**: 20m (smaller = more detailed, longer flight)
- Click **"Create & Start Mission"**
- Drone will execute autonomously

#### 3. Monitor Flight
- Watch real-time telemetry in Status Panel
- View drone position on Map
- Monitor battery level

#### 4. Return Home
- Click **"🏠 Return to Launch"** to end mission
- Or mission auto-lands when battery is low

#### 5. Disarm
- Click **"✗ Disarm"** after landing

## 📊 Understanding the Analysis

### NDVI (Vegetation Index)
- **0.0 - 0.3**: No vegetation / Dead crop
- **0.3 - 0.5**: Sparse / Stressed vegetation
- **0.5 - 0.7**: Healthy vegetation
- **0.7 - 1.0**: Very healthy / Dense vegetation

**Action:**
- < 0.3: Increase irrigation or check for disease
- 0.3-0.5: Monitor closely, adjust water/nutrients
- > 0.6: Excellent, maintain current schedule

### Disease Detection
System identifies:
- 🔴 Powdery Mildew
- 🟠 Leaf Spot
- 🟡 Rust
- 🟣 Blight
- 🟢 Mosaic Virus

**When detected:**
- Follow treatment recommendations
- Reduce affected area moisture
- Apply appropriate fungicide/pesticide

## 📍 Mission Planning Tips

### Survey Area Selection

**Latitude/Longitude:**
- Use GPS coordinates or maps
- Center point of your field
- Addis Ababa: 9.0320°N, 38.7469°E

**Altitude:**
- **30-50m**: High resolution, longer flight
- **50-100m**: Good balance, moderate resolution
- **100m+**: Wide area, lower resolution

**Grid Spacing:**
- **10m**: Ultra-detailed (good for small fields)
- **20m**: Standard (recommended)
- **30m+**: Low resolution (large areas only)

### Example Missions

**Small Farm (2-5 hectares):**
- Altitude: 50m
- Grid Spacing: 15m
- Flight Time: ~15 min

**Large Farm (10-20 hectares):**
- Altitude: 100m
- Grid Spacing: 30m
- Flight Time: ~20 min

**Disaster Assessment:**
- Altitude: 80m
- Grid Spacing: 25m
- Priority: Speed over detail

## 📱 Real-Time Monitoring

### Dashboard Updates
- Battery: Updates every 2 seconds
- Altitude: Real-time tracking
- Position: Live GPS coordinates
- Status: Armed/Flying/Landed

### Alerts
- 🟢 Green: All systems normal
- 🟡 Yellow: Warning (low battery)
- 🔴 Red: Critical (emergency)

## 🛰️ Advanced Features

### Exporting Data
```bash
# Get flight logs
curl http://localhost:8000/logs

# Generate report
curl -X POST http://localhost:8000/reports/generate?mission_id=MISSION-0001
```

### API Usage

**Create Mission (Python):**
```python
import requests

config = {
    "mission_name": "Field Survey",
    "latitude": 9.0320,
    "longitude": 38.7469,
    "altitude": 50,
    "grid_spacing": 20
}

response = requests.post(
    "http://localhost:8000/missions/create",
    json=config
)
print(response.json())
```

## 🔐 Safety Guidelines

### Pre-Flight Checklist
- ✅ Battery > 50%
- ✅ GPS lock acquired
- ✅ Weather: Calm winds
- ✅ Airspace: Clear of obstacles
- ✅ Area: Authorized for flight

### In-Flight Safety
- ✅ Keep visual line of sight
- ✅ Monitor battery status
- ✅ Be ready to RTL if needed
- ✅ Avoid flying over people

### Post-Flight
- ✅ Download mission data
- ✅ Check battery condition
- ✅ Review analysis results
- ✅ Generate reports

## 🌾 Agricultural Applications

### 1. Crop Health Monitoring
- Detect stress early
- Monitor growth stages
- Verify fertilizer effectiveness

### 2. Disease Detection
- Identify infections
- Map affected areas
- Plan treatment

### 3. Irrigation Optimization
- Check water stress
- Optimize scheduling
- Reduce water usage

### 4. Pest Management
- Monitor infestation levels
- Plan spraying routes
- Verify treatment effectiveness

### 5. Yield Prediction
- Estimate crop yield
- Plan harvest
- Optimize resource allocation

## 📞 Support & Help

### Documentation
- API Docs: http://localhost:8000/docs
- GitHub: https://github.com/biniyamt1629/eduability
- README: See project README.md

### Common Issues

**Q: Drone won't arm**
A: Check battery > 20%, GPS signal acquired

**Q: Mission won't start**
A: Drone must be armed, check coordinates format

**Q: Analysis shows no data**
A: Need actual flight data, simulator shows sample data

---

**Happy Flying! 🚁 Enjoy your agricultural monitoring!**