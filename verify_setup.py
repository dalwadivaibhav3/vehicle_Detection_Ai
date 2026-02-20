import os
import sys
import pymysql
from ultralytics import YOLO

def verify_setup():
    print("--- Environment Verification ---")
    
    # Check directories
    folders = ['static/uploads', 'static/videos', 'models']
    for folder in folders:
        if os.path.exists(folder):
            print(f"[OK] Directory exists: {folder}")
        else:
            print(f"[ERROR] Directory missing: {folder}")
            os.makedirs(folder, exist_ok=True)
            print(f"      Created: {folder}")
            
    # Check Database
    try:
        conn = pymysql.connect(host='localhost', user='root', password='')
        print("[OK] MySQL Connection successful")
        conn.close()
    except Exception as e:
        print(f"[ERROR] MySQL Connection failed: {e}")
        
    # Check YOLO Model
    try:
        model = YOLO('yolov8n.pt')
        print("[OK] YOLOv8 Model loaded successfully")
    except Exception as e:
        print(f"[ERROR] YOLOv8 Model load failed: {e}")

if __name__ == "__main__":
    # Ensure we are in the right directory
    base_dir = r'c:\Users\Vaibhav\OneDrive\Desktop\traffic_vehicle_detection_demo\traffic_vehicle_detection'
    os.chdir(base_dir)
    verify_setup()
