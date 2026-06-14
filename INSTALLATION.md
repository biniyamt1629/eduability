# DroneMapper Ethiopia - Installation & Setup Guide

## 🚀 Quick Start (5 minutes)

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/biniyamt1629/eduability.git
cd eduability

# Start all services
docker-compose up -d

# Access:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8+
- Node.js 14+
- pip
- git

#### Backend Setup

```bash
# Navigate to project
cd eduability

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python backend/main.py
```

Backend runs on: http://localhost:8000

#### Frontend Setup

```bash
# Open frontend in browser
# Simply open: frontend/index.html in your browser
# Or use Python's built-in server:

python -m http.server 3000 --directory frontend
```

Frontend runs on: http://localhost:3000

## 📋 Project Structure

```
edibility/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── flight_control/         # Autopilot system
│   ├── mission_planning/       # Mission generator
│   ├── image_processing/       # NDVI & Disease detection
│   └── data_handler/           # Logging & data
├── frontend/
│   └── index.html             # Web dashboard
├── requirements.txt           # Python dependencies
├── docker-compose.yml        # Docker configuration
├── Dockerfile               # Container image
└── README.md               # Documentation
```

## 🧪 Testing the System

### 1. Check API Health
```bash
curl http://localhost:8000/health
```

### 2. Access Dashboard
Open http://localhost:3000 in your browser

### 3. Arm Drone
Click "Arm Drone" button in dashboard

### 4. Create Mission
- Fill in mission parameters
- Click "Create & Start Mission"
- Watch drone fly in simulation

## 🔧 Configuration

### Drone Parameters
Edit `backend/flight_control/autopilot.py`:
```python
self.latitude = 9.0320   # Addis Ababa coordinates
self.longitude = 38.7469
```

### Mission Parameters
In frontend/index.html:
```javascript
// Default mission area
latitude: 9.0320
longitude: 38.7469
altitude: 50  // meters
grid_spacing: 20  // meters
```

## 📊 API Endpoints

### Drone Control
- `POST /drone/arm` - Arm drone
- `POST /drone/disarm` - Disarm drone
- `POST /drone/rtl` - Return to launch
- `GET /drone/status` - Get drone status

### Missions
- `POST /missions/create` - Create new mission
- `POST /missions/{id}/start` - Start mission
- `GET /missions/{id}` - Get mission details

### Image Analysis
- `POST /images/analyze` - Analyze image for crop health
- `POST /reports/generate` - Generate mission report

## 📈 Viewing Results

1. **Dashboard**: Open http://localhost:3000
2. **API Documentation**: http://localhost:8000/docs
3. **Logs**: Check browser console for real-time updates

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### CORS Issues
Backend has CORS enabled for all origins (development mode)

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 🚀 Deployment

### Production Deployment

```bash
# Build Docker image
docker build -t dronemapper-ethiopia .

# Run container
docker run -p 8000:8000 dronemapper-ethiopia
```

## 📞 Support

For issues or questions:
1. Check documentation
2. Review API docs at http://localhost:8000/docs
3. Check logs in console

---

**Happy Flying! 🚁**