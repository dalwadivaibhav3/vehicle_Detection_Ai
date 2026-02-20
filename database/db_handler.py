import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, host='localhost', user='root', password='', database='traffic_detection'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def get_connection(self):
        """Get database connection"""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    # User Management Functions
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            hashed_password = generate_password_hash(password)
            
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password))
            connection.commit()
            
            cursor.close()
            connection.close()
            return True, "Registration successful!"
        except pymysql.err.IntegrityError:
            return False, "Username or email already exists!"
        except Exception as e:
            print(f"Registration error: {e}")
            return False, f"Error: {str(e)}"
    
    def login_user(self, username, password):
        """Authenticate user login"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if user and check_password_hash(user['password'], password):
                return True, user
            else:
                return False, None
        except Exception as e:
            return False, None
    
    # Video Management Functions
    def save_video_upload(self, user_id, video_name, video_path):
        """Save video upload information"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "INSERT INTO video_uploads (user_id, video_name, video_path) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, video_name, video_path))
            connection.commit()
            
            video_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            return True, video_id
        except Exception as e:
            return False, None
    
    def update_video_status(self, video_id, status):
        """Update video processing status"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "UPDATE video_uploads SET processing_status = %s WHERE id = %s"
            cursor.execute(query, (status, video_id))
            connection.commit()
            
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Update video status error: {e}")
            return False
    
    def save_vehicle_counts(self, video_id, counts):
        """Save vehicle detection results"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            total = sum(counts.values())
            
            query = """
                INSERT INTO vehicle_counts 
                (video_id, bike_count, activa_count, car_count, bus_count, truck_count, cycle_count, rickshaw_count, total_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                video_id,
                counts.get('bike', 0),
                counts.get('activa', 0),
                counts.get('car', 0),
                counts.get('bus', 0),
                counts.get('truck', 0),
                counts.get('cycle', 0),
                counts.get('rickshaw', 0),
                total
            ))
            connection.commit()
            
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error saving counts: {e}")
            return False
    
    def get_user_videos(self, user_id):
        """Get all videos uploaded by a user"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
                SELECT 
                    v.id, v.user_id, v.video_name, v.video_path, v.upload_time, v.processing_status,
                    vc.bike_count, vc.activa_count, vc.car_count, vc.bus_count, vc.truck_count, 
                    vc.cycle_count, vc.rickshaw_count, vc.total_count, vc.processed_at
                FROM video_uploads v
                LEFT JOIN vehicle_counts vc ON v.id = vc.video_id
                WHERE v.user_id = %s
                ORDER BY v.upload_time DESC
            """
            cursor.execute(query, (user_id,))
            videos = cursor.fetchall()
            
            cursor.close()
            connection.close()
            return videos
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return []
    
    def get_latest_result(self, user_id):
        """Get the latest processing result for a user"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
                SELECT 
                    v.id, v.user_id, v.video_name, v.video_path, v.upload_time, v.processing_status,
                    vc.bike_count, vc.activa_count, vc.car_count, vc.bus_count, vc.truck_count, 
                    vc.cycle_count, vc.rickshaw_count, vc.total_count, vc.processed_at
                FROM video_uploads v
                LEFT JOIN vehicle_counts vc ON v.id = vc.video_id
                WHERE v.user_id = %s AND v.processing_status = 'completed'
                ORDER BY v.upload_time DESC
                LIMIT 1
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            return result
        except Exception as e:
            print(f"Error fetching result: {e}")
            return None
