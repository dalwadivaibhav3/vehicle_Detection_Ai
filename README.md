# Traffic Vehicle Detection and Counting System

An AI-powered web application for automatic vehicle detection and counting from traffic videos using YOLOv8 deep learning model.

## 🚀 Features

- **User Authentication**: Secure registration and login system
- **Video Upload**: Support for multiple video formats (MP4, AVI, MOV, MKV)
- **AI-Powered Detection**: YOLOv8-based vehicle detection and classification
- **Real-time Processing**: Background video processing with status tracking
- **Vehicle Classification**: Detects and counts:
  - Bikes (Motorcycles)
  - Cars
  - Buses
  - Trucks
  - Cycles (Bicycles)
- **Interactive Dashboard**: Visual representation of results with charts
- **Processing History**: Track all uploaded and processed videos
- **Detailed Analytics**: Comprehensive statistics and visualizations

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- MySQL Database
- 4GB RAM minimum (8GB recommended)
- GPU (Optional, but recommended for faster processing)

### Software Dependencies
- Flask (Web Framework)
- YOLOv8 (Vehicle Detection)
- OpenCV (Video Processing)
- PyMySQL (Database)
- Bootstrap 5 (Frontend)

## 🔧 Installation

### Step 1: Clone or Download the Project
```bash
git clone <repository-url>
cd traffic_vehicle_detection
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

1. Install MySQL Server (if not already installed)
2. Create a new database:
```sql
CREATE DATABASE traffic_detection;
```

3. Update database credentials in `database/db_setup.py` and `database/db_handler.py`:
```python
host='localhost'
user='root'
password='your_password'  # Change this
database='traffic_detection'
```

### Step 5: Initialize Database Tables
```bash
python database/db_setup.py
```

### Step 6: Download YOLOv8 Model

The YOLOv8 model will be automatically downloaded on first run. Alternatively, you can download it manually:
```bash
# This happens automatically when you first run the detection
# No manual download needed
```

### Step 7: Create Required Directories
```bash
mkdir -p static/uploads static/videos
```

## 🚀 Running the Application

### Development Mode
```bash
python app.py
```

The application will start at: `http://localhost:5000`

### Production Mode (Using Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📖 Usage Guide

### 1. User Registration
- Navigate to `http://localhost:5000`
- Click "Register here"
- Fill in username, email, and password
- Click "Register"

### 2. Login
- Enter your username and password
- Click "Login"

### 3. Upload Video
- Click "Select Traffic Video"
- Choose a video file (MP4, AVI, MOV, or MKV)
- Click "Upload Video"

### 4. Process Video
- After upload, find your video in the "Processing History" table
- Click the "Process" button
- Wait for processing to complete (this may take several minutes)

### 5. View Results
- Once processing is complete, click "View" button
- See detailed statistics and visualizations
- View vehicle counts by type
- Analyze distribution charts

## 📁 Project Structure

```
traffic_vehicle_detection/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/
│   ├── db_setup.py            # Database initialization
│   └── db_handler.py          # Database operations
│
├── models/
│   └── vehicle_detector.py    # YOLOv8 detection module
│
├── templates/
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   └── results.html           # Results display
│
└── static/
    ├── css/
    │   └── style.css          # Custom styles
    ├── js/
    │   ├── main.js            # Common JavaScript
    │   └── dashboard.js       # Dashboard functionality
    ├── uploads/               # Uploaded videos
    └── videos/                # Processed videos
```

## 🔍 How It Works

### Vehicle Detection Process

1. **Video Upload**: User uploads a traffic video
2. **Frame Extraction**: System extracts frames from the video
3. **AI Detection**: YOLOv8 model detects vehicles in each frame
4. **Object Tracking**: Custom tracking algorithm assigns unique IDs to vehicles
5. **Counting**: Vehicles crossing the counting line are counted once
6. **Classification**: Vehicles are classified into 5 categories
7. **Results Storage**: Final counts are saved to database
8. **Visualization**: Results are displayed with charts and statistics

### Vehicle Classification

The system uses YOLOv8 pre-trained on COCO dataset and maps the following classes:
- `motorcycle` → Bike
- `car` → Car
- `bus` → Bus
- `truck` → Truck
- `bicycle` → Cycle

## 🎨 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Web framework
- **YOLOv8**: Object detection model
- **OpenCV**: Video processing
- **PyMySQL**: Database connectivity

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling
- **Bootstrap 5**: Responsive design
- **JavaScript**: Interactivity
- **Chart.js**: Data visualization

### Database
- **MySQL**: Data storage

## ⚙️ Configuration

### Database Configuration
Edit `database/db_handler.py`:
```python
class Database:
    def __init__(self, 
                 host='localhost',
                 user='root',
                 password='YOUR_PASSWORD',
                 database='traffic_detection'):
```

### Upload Configuration
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Max file size
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}     # Allowed formats
```

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check database credentials
- Ensure database exists

### Video Upload Fails
- Check file size (max 500MB)
- Verify file format
- Ensure uploads directory exists

### Processing Takes Too Long
- Use GPU for faster processing
- Process smaller videos
- Reduce video resolution

### Model Not Found
- YOLOv8 will download automatically on first run
- Check internet connection
- Manually download from Ultralytics

## 📊 Performance Tips

1. **Use GPU**: Install CUDA-enabled PyTorch for faster processing
2. **Optimize Video**: Lower resolution videos process faster
3. **Batch Processing**: Process multiple videos sequentially
4. **Cache Results**: Already processed videos don't need reprocessing

## 🔐 Security Notes

- Change the Flask secret key in production
- Use environment variables for sensitive data
- Implement HTTPS in production
- Add rate limiting for API endpoints
- Validate all user inputs

## 📝 Future Enhancements

- [ ] Real-time video stream processing
- [ ] Multiple counting lines
- [ ] Vehicle speed detection
- [ ] License plate recognition
- [ ] Traffic flow analysis
- [ ] Mobile app integration
- [ ] Export reports to PDF/Excel
- [ ] Multi-user dashboard
- [ ] Admin panel

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes.

## 👥 Authors

- Your Name
- Institution/Organization

## 📧 Contact

For questions or support, contact: your.email@example.com

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV Community
- Flask Framework
- Bootstrap Team

---

**Note**: This system is designed for educational and research purposes. For production deployment, additional security measures and optimizations are recommended.
