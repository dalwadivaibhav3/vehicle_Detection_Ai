from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
import os
import time
from datetime import timedelta
import threading

# Import custom modules
from database.db_handler import Database
from models.vehicle_detector import VehicleDetector

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/videos'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Database instance
db = Database()

# Global processing status
processing_status = {}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video_background(video_id, video_path, user_id):
    """Background thread function to process video"""
    global processing_status
    
    try:
        processing_status[video_id] = {'status': 'processing', 'progress': 0}
        db.update_video_status(video_id, 'processing')
        
        # Initialize detector
        detector = VehicleDetector()
        
        # Output path
        output_filename = f"processed_{video_id}.mp4"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        # Process video
        success, counts = detector.process_video(video_path, output_path, show_preview=False)
        
        if success:
            # Save results to database
            db.save_vehicle_counts(video_id, counts)
            db.update_video_status(video_id, 'completed')
            processing_status[video_id] = {'status': 'completed', 'progress': 100, 'counts': counts}
        else:
            db.update_video_status(video_id, 'failed')
            processing_status[video_id] = {'status': 'failed', 'progress': 0}
            
    except Exception as e:
        import traceback
        print(f"Error processing video {video_id}: {e}")
        traceback.print_exc()
        db.update_video_status(video_id, 'failed')
        processing_status[video_id] = {'status': 'failed', 'progress': 0, 'error': str(e)}

@app.route('/')
def index():
    """Home page - redirect to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return render_template('register.html')
        
        # Register user
        success, message = db.register_user(username, email, password)
        
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return render_template('login.html')
        
        success, user = db.login_user(username, password)
        
        if success:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    if 'user_id' not in session:
        flash('Please login to access the dashboard!', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get user's videos
    videos = db.get_user_videos(user_id)
    
    # Get latest result
    latest_result = db.get_latest_result(user_id)
    if latest_result:
        # Ensure filename is just the basename
        latest_result['video_filename'] = os.path.basename(latest_result['video_path'])
    
    # Process video list to include filenames
    for v in videos:
        v['video_filename'] = os.path.basename(v['video_path'])
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         videos=videos,
                         latest_result=latest_result)

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video upload"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    if 'video' not in request.files:
        return jsonify({'success': False, 'message': 'No video file uploaded'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file type. Allowed: mp4, avi, mov, mkv'}), 400
    
    try:
        # Secure filename
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        unique_filename = f"{timestamp}_{filename}"
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Save to database
        user_id = session['user_id']
        success, video_id = db.save_video_upload(user_id, filename, filepath)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Video uploaded successfully!',
                'video_id': video_id
            })
        else:
            return jsonify({'success': False, 'message': 'Database error'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/process/<int:video_id>', methods=['POST'])
def process_video(video_id):
    """Start video processing"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        # Get video info
        videos = db.get_user_videos(session['user_id'])
        video = next((v for v in videos if v['id'] == video_id), None)
        
        if not video:
            return jsonify({'success': False, 'message': 'Video not found'}), 404
        
        video_path = video['video_path']
        
        # Start background processing
        thread = threading.Thread(
            target=process_video_background,
            args=(video_id, video_path, session['user_id'])
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Processing started!',
            'video_id': video_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/status/<int:video_id>')
def get_status(video_id):
    """Get processing status"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    status = processing_status.get(video_id, {'status': 'pending', 'progress': 0})
    return jsonify(status)

@app.route('/results/<int:video_id>')
def view_results(video_id):
    """View processing results"""
    if 'user_id' not in session:
        flash('Please login to view results!', 'warning')
        return redirect(url_for('login'))
    
    videos = db.get_user_videos(session['user_id'])
    video = next((v for v in videos if v['id'] == video_id), None)
    
    if not video:
        flash('Video not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Add simple filenames
    video['video_filename'] = os.path.basename(video['video_path'])
    
    return render_template('results.html', video=video, username=session['username'])

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    
    # Run application
    app.run(debug=True, host='0.0.0.0', port=5000)
