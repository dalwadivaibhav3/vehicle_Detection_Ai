import pymysql
from datetime import datetime

class DatabaseSetup:
    def __init__(self, host='localhost', user='root', password='', database='traffic_detection'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def create_database(self):
        """Create the database if it doesn't exist"""
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"Database '{self.database}' created successfully!")
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error creating database: {e}")
    
    def create_tables(self):
        """Create all required tables"""
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Video uploads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS video_uploads (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    video_name VARCHAR(255) NOT NULL,
                    video_path VARCHAR(500) NOT NULL,
                    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processing_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Vehicle count results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicle_counts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    video_id INT NOT NULL,
                    bike_count INT DEFAULT 0,
                    activa_count INT DEFAULT 0,
                    car_count INT DEFAULT 0,
                    bus_count INT DEFAULT 0,
                    truck_count INT DEFAULT 0,
                    cycle_count INT DEFAULT 0,
                    rickshaw_count INT DEFAULT 0,
                    total_count INT DEFAULT 0,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES video_uploads(id) ON DELETE CASCADE
                )
            """)
            
            connection.commit()
            print("All tables created successfully!")
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    # Initialize and setup database
    db_setup = DatabaseSetup(
        host='localhost',
        user='root',
        password='',  # Update with your MySQL password
        database='traffic_detection'
    )
    
    db_setup.create_database()
    db_setup.create_tables()
