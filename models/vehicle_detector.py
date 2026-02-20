import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
import time

class VehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initialize the vehicle detector with YOLOv8 model
        """
        self.model = YOLO(model_path)
        
        # Vehicle class mapping (COCO dataset classes)
        self.vehicle_classes = {
            'bicycle': 'cycle',
            'car': 'car',
            'motorcycle': 'bike', # Using bike for motorcycle
            'bus': 'bus',
            'truck': 'truck'
        }
        
        # Vehicle counts
        self.vehicle_counts = {
            'bike': 0,
            'activa': 0,
            'car': 0,
            'bus': 0,
            'truck': 0,
            'cycle': 0,
            'rickshaw': 0
        }
        
        # Tracking information
        self.tracked_objects = {}
        self.next_object_id = 0
        self.max_disappeared = 30
        
    def get_center(self, box):
        """Calculate center point of bounding box"""
        x1, y1, x2, y2 = box
        return (int((x1 + x2) / 2), int((y1 + y2) / 2))
    
    def register_object(self, centroid, vehicle_type):
        """Register a new tracked object"""
        self.tracked_objects[self.next_object_id] = {
            'centroid': centroid,
            'type': vehicle_type,
            'disappeared': 0,
            'counted': False
        }
        self.next_object_id += 1
    
    def update_tracking(self, centroids, vehicle_types):
        """Update object tracking"""
        if len(self.tracked_objects) == 0:
            for i, centroid in enumerate(centroids):
                self.register_object(centroid, vehicle_types[i])
        else:
            object_ids = list(self.tracked_objects.keys())
            object_centroids = [self.tracked_objects[oid]['centroid'] for oid in object_ids]
            
            if len(centroids) == 0:
                for object_id in object_ids:
                    self.tracked_objects[object_id]['disappeared'] += 1
                    if self.tracked_objects[object_id]['disappeared'] > self.max_disappeared:
                        del self.tracked_objects[object_id]
            else:
                # Simple distance-based tracking
                for i, centroid in enumerate(centroids):
                    min_distance = float('inf')
                    closest_id = None
                    
                    for oid, obj_centroid in zip(object_ids, object_centroids):
                        distance = np.linalg.norm(np.array(centroid) - np.array(obj_centroid))
                        if distance < min_distance:
                            min_distance = distance
                            closest_id = oid
                    
                    if min_distance < 80:  # Increased threshold for better tracking
                        self.tracked_objects[closest_id]['centroid'] = centroid
                        self.tracked_objects[closest_id]['disappeared'] = 0
                        
                        # Count if crossing counting line and not already counted
                        if not self.tracked_objects[closest_id]['counted']:
                            vehicle_type = self.tracked_objects[closest_id]['type']
                            # Counting line is now dynamic (set during process_video)
                            line_y = getattr(self, 'counting_line_y', 300)
                            if centroid[1] > line_y:
                                self.vehicle_counts[vehicle_type] += 1
                                self.tracked_objects[closest_id]['counted'] = True
                    else:
                        self.register_object(centroid, vehicle_types[i])
    
    def detect_vehicles(self, frame):
        """Detect vehicles in a single frame"""
        results = self.model(frame, conf=0.3, verbose=False)
        
        centroids = []
        vehicle_types = []
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class name
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                # Check if it's a vehicle we're tracking
                if class_name in self.vehicle_classes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    
                    vehicle_type = self.vehicle_classes[class_name]
                    
                    # Heuristic for demo: Distinguish Activa from Bike and Rickshaw from Car
                    if vehicle_type == 'bike' and confidence > 0.6:
                        vehicle_type = 'activa'
                    elif vehicle_type == 'car' and (x2 - x1) / (y2 - y1) < 1.0: # Narrower than usual car
                        vehicle_type = 'rickshaw'
                        
                    centroid = self.get_center([x1, y1, x2, y2])
                    
                    centroids.append(centroid)
                    vehicle_types.append(vehicle_type)
                    
                    detections.append({
                        'box': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': confidence,
                        'type': vehicle_type,
                        'centroid': centroid
                    })
        
        # Update tracking
        self.update_tracking(centroids, vehicle_types)
        
        return detections
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        # Draw counting line (dynamic height)
        line_y = getattr(self, 'counting_line_y', int(frame.shape[0] * 0.6))
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 255), 3)
        cv2.putText(frame, "COUNTING LINE", (10, line_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Draw detections
        for detection in detections:
            x1, y1, x2, y2 = detection['box']
            vehicle_type = detection['type']
            confidence = detection['confidence']
            
            # Color coding for different vehicles
            colors = {
                'bike': (255, 0, 0),      # Blue
                'activa': (255, 255, 0),  # Cyan
                'car': (0, 255, 0),       # Green
                'bus': (0, 0, 255),       # Red
                'truck': (255, 0, 255),   # Magenta
                'cycle': (0, 255, 255),   # Yellow
                'rickshaw': (128, 0, 128) # Purple
            }
            
            color = colors.get(vehicle_type, (255, 255, 255))
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{vehicle_type}: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Draw center point
            cv2.circle(frame, detection['centroid'], 4, color, -1)
        
        # Draw counts
        y_offset = 30
        for vehicle_type, count in self.vehicle_counts.items():
            text = f"{vehicle_type.capitalize()}: {count}"
            cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30
        
        return frame
    
    def process_video(self, video_path, output_path=None, show_preview=False):
        """Process entire video and count vehicles"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return False, "Error opening video file"
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Set counting line at 60% of frame height
        self.counting_line_y = int(height * 0.6)
        
        # Video writer
        if output_path:
            # Try 'H264' for best browser compatibility, fallback to 'mp4v'
            try:
                fourcc = cv2.VideoWriter_fourcc(*'H264')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                if not out.isOpened():
                    raise Exception("H264 failed")
            except:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        last_detections = []
        
        print(f"Processing video: {total_frames} frames at {fps} FPS")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Detect every frame for best accuracy, or every 2nd frame if performance is an issue
            # But ALWAYS draw on every frame using last_detections
            if frame_count % 1 == 0: # Check every frame
                last_detections = self.detect_vehicles(frame)
            
            # Always draw detections on the frame
            frame = self.draw_detections(frame, last_detections)
            
            # Write frame
            if output_path:
                out.write(frame)
            
            # Show preview
            if show_preview:
                cv2.imshow('Vehicle Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Progress
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.2f}% - Frames: {frame_count}/{total_frames}")
        
        cap.release()
        if output_path:
            out.release()
        if show_preview:
            cv2.destroyAllWindows()
        
        print("Processing completed!")
        print(f"Final Counts: {self.vehicle_counts}")
        
        return True, self.vehicle_counts
    
    def reset_counts(self):
        """Reset all vehicle counts"""
        self.vehicle_counts = {
            'bike': 0,
            'activa': 0,
            'car': 0,
            'bus': 0,
            'truck': 0,
            'cycle': 0,
            'rickshaw': 0
        }
        self.tracked_objects = {}
        self.next_object_id = 0

# Test function
if __name__ == "__main__":
    detector = VehicleDetector()
    success, counts = detector.process_video("test_video.mp4", "output_video.mp4", show_preview=True)
    
    if success:
        print("\nVehicle Counts:")
        for vehicle_type, count in counts.items():
            print(f"{vehicle_type.capitalize()}: {count}")
