# Quick Installation Guide

## Prerequisites
- Python 3.8 or higher
- MySQL Server
- 4GB RAM minimum
- 10GB free disk space

## Installation Steps

### 1. Download/Clone Project
```bash
# If using git
git clone <repository-url>
cd traffic_vehicle_detection

# Or download and extract ZIP file
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database

#### Option A: Using MySQL Command Line
```sql
CREATE DATABASE traffic_detection;
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Create new schema named "traffic_detection"

### 5. Configure Database
Edit the files with your MySQL credentials:

**database/db_setup.py:**
```python
db_setup = DatabaseSetup(
    host='localhost',
    user='root',
    password='YOUR_PASSWORD',  # Change this
    database='traffic_detection'
)
```

**database/db_handler.py:**
```python
def __init__(self, 
             host='localhost',
             user='root',
             password='YOUR_PASSWORD',  # Change this
             database='traffic_detection'):
```

### 6. Initialize Database Tables
```bash
python database/db_setup.py
```

You should see:
```
Database 'traffic_detection' created successfully!
All tables created successfully!
```

### 7. Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 8. Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL Server running
- [ ] Virtual environment activated
- [ ] Dependencies installed (no errors)
- [ ] Database created
- [ ] Tables created successfully
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can register new user
- [ ] Can login successfully

## Common Installation Issues

### Issue 1: Python not found
**Solution:** Install Python from python.org or use system package manager

### Issue 2: pip not found
**Solution:** 
```bash
python -m ensurepip --upgrade
```

### Issue 3: MySQL connection failed
**Solutions:**
- Check MySQL service is running
- Verify username/password
- Check port 3306 is not blocked

### Issue 4: Module not found errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue 5: Port 5000 already in use
**Solution:** Change port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

## First-Time Setup Commands (Copy-Paste Ready)

### For Windows:
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python database\db_setup.py
python app.py
```

### For Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python database/db_setup.py
python app.py
```

## Default Login (After Creating Account)
- Create your account through the web interface
- No default credentials provided for security

## Directory Structure After Installation
```
traffic_vehicle_detection/
├── app.py                     ✓ Main application
├── requirements.txt           ✓ Dependencies
├── README.md                  ✓ Documentation
├── database/
│   ├── db_setup.py           ✓ Database setup
│   └── db_handler.py         ✓ Database operations
├── models/
│   └── vehicle_detector.py   ✓ AI detection
├── templates/                 ✓ HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── results.html
├── static/
│   ├── css/
│   │   └── style.css         ✓ Styles
│   ├── js/
│   │   ├── main.js           ✓ Common JS
│   │   └── dashboard.js      ✓ Dashboard JS
│   ├── uploads/              ✓ Video uploads (created)
│   └── videos/               ✓ Processed videos (created)
└── venv/                      ✓ Virtual environment
```

## Next Steps

1. **Register an Account**
   - Go to http://localhost:5000
   - Click "Register here"
   - Create your account

2. **Upload a Test Video**
   - Login with your credentials
   - Upload a traffic video
   - Click "Process"

3. **View Results**
   - Wait for processing to complete
   - Click "View" to see detailed results

## Support

- Check USER_MANUAL.md for usage instructions
- See DOCUMENTATION.md for technical details
- Review README.md for project overview

## Production Deployment

For production use:
1. Change Flask secret key in app.py
2. Set DEBUG=False
3. Use production WSGI server (Gunicorn)
4. Setup Nginx reverse proxy
5. Configure SSL/HTTPS
6. Setup proper backups
7. Configure firewall rules

Quick production command:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Installation Complete! 🎉**

You're now ready to use the Traffic Vehicle Detection System!
