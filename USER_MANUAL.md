# Traffic Vehicle Detection System - User Manual

## Quick Start Guide

### 1. Getting Started

#### System Requirements
- Web browser (Chrome, Firefox, Safari, or Edge)
- Internet connection
- Video files in MP4, AVI, MOV, or MKV format

#### Accessing the System
1. Open your web browser
2. Navigate to: `http://localhost:5000` (or your deployed URL)
3. You will see the login page

---

### 2. User Registration

#### First Time Users
1. Click on "Register here" link on the login page
2. Fill in the registration form:
   - **Username**: Choose a unique username (letters, numbers, underscore)
   - **Email**: Enter your valid email address
   - **Password**: Create a strong password (minimum 6 characters)
   - **Confirm Password**: Re-enter your password
3. Click the "Register" button
4. You will be redirected to the login page with a success message

#### Registration Tips
- Choose a memorable username
- Use a strong password with mix of letters and numbers
- Keep your login credentials safe

---

### 3. Logging In

1. Enter your username in the "Username" field
2. Enter your password in the "Password" field
3. Click the "Login" button
4. You will be redirected to the dashboard

---

### 4. Dashboard Overview

After logging in, you'll see the main dashboard with three main sections:

#### A. Upload Section (Left)
- **Video Selection**: Browse and select traffic video files
- **Video Preview**: Preview your selected video before upload
- **Upload Button**: Upload the video to the system

#### B. Latest Results (Right)
- **Quick Stats**: See your most recent analysis results
- **Vehicle Counts**: View counts for each vehicle type
- **View Details**: Access comprehensive results

#### C. Processing History (Bottom)
- **Video List**: All your uploaded videos
- **Status**: Current processing status of each video
- **Actions**: Process pending videos or view completed results

---

### 5. Uploading a Traffic Video

#### Step-by-Step Upload Process

1. **Select Video File**
   - Click "Select Traffic Video" button
   - Browse your computer for a traffic video
   - Supported formats: MP4, AVI, MOV, MKV
   - Maximum file size: 500MB

2. **Preview Video** (Optional)
   - After selection, video preview appears automatically
   - You can play the video to verify it's correct

3. **Upload**
   - Click "Upload Video" button
   - Wait for upload progress bar to complete
   - Success message will appear when upload is complete

4. **Upload Confirmation**
   - Your video appears in the "Processing History" table
   - Status shows as "Pending"
   - You can now process the video

#### Upload Tips
- Use clear, good quality videos for best results
- Ensure video shows road traffic clearly
- Avoid videos with too much motion blur
- Compress large videos before uploading if needed

---

### 6. Processing a Video

#### Starting Video Analysis

1. **Locate Your Video**
   - Find your uploaded video in "Processing History" table
   - Check that status is "Pending"

2. **Start Processing**
   - Click the blue "Process" button
   - Confirm the processing start
   - Button changes to "Processing" with spinning icon

3. **Wait for Completion**
   - Processing time depends on video length
   - Typically 2-10 minutes for standard videos
   - Status updates automatically
   - You can leave the page and come back later

4. **Processing Complete**
   - Status changes to "Completed" (green badge)
   - "View" button becomes available
   - Results appear in "Latest Results" section

#### Processing Tips
- Process one video at a time for faster results
- Longer videos take more time to process
- Don't close the browser completely during processing
- You'll receive notification when processing completes

---

### 7. Viewing Results

#### Accessing Detailed Results

1. **From Dashboard**
   - Click "View" button next to completed video in history
   - OR click "View Detailed Results" in Latest Results section

2. **Results Page Components**

   **A. Video Information**
   - Video name
   - Upload time
   - Processing completion time

   **B. Vehicle Count Cards**
   - Individual count cards for each vehicle type:
     - 🏍️ Bikes (Motorcycles)
     - 🚗 Cars
     - 🚌 Buses
     - 🚛 Trucks
     - 🚴 Cycles (Bicycles)
     - 🧮 Total count

   **C. Visual Charts**
   - **Pie Chart**: Shows distribution of vehicle types
   - **Bar Chart**: Compares counts across categories

   **D. Statistics Table**
   - Detailed breakdown with percentages
   - Visual progress bars
   - Complete analysis data

#### Understanding the Results

- **Bike Count**: Motorcycles and scooters
- **Car Count**: Personal vehicles and small cars
- **Bus Count**: Buses and large passenger vehicles
- **Truck Count**: Cargo trucks and large vehicles
- **Cycle Count**: Bicycles
- **Total Count**: Sum of all detected vehicles

---

### 8. Managing Your Videos

#### Video History

All your uploaded videos are listed in the Processing History table:

- **Video Name**: Original filename
- **Upload Time**: When you uploaded it
- **Status**: Current processing state
  - 🔘 Pending: Ready to process
  - ⚠️ Processing: Currently being analyzed
  - ✅ Completed: Analysis finished
  - ❌ Failed: Processing error occurred

- **Total Count**: Number of vehicles detected
- **Actions**: Available operations

#### Deleting Videos

Currently, videos remain in your history. Future updates will include:
- Delete individual videos
- Clear all history
- Export results

---

### 9. Understanding Vehicle Detection

#### How It Works

The system uses AI (Artificial Intelligence) to:

1. **Analyze Video**: Breaks video into individual frames
2. **Detect Vehicles**: Identifies vehicles in each frame
3. **Classify Types**: Categorizes each vehicle
4. **Track Movement**: Follows vehicles across frames
5. **Count Accurately**: Prevents duplicate counting
6. **Generate Results**: Creates comprehensive statistics

#### Detection Accuracy

- Uses advanced YOLOv8 AI model
- Pre-trained on thousands of traffic images
- Typical accuracy: 85-95%
- Better results with:
  - Clear, high-quality videos
  - Good lighting conditions
  - Minimal obstruction
  - Stable camera position

---

### 10. Best Practices

#### For Best Results

**Video Quality**
- Use HD or higher resolution
- Ensure good lighting
- Avoid heavy rain/fog conditions
- Stable camera mounting

**Video Content**
- Clear view of traffic
- Minimal obstructions
- Consistent camera angle
- Representative traffic sample

**File Management**
- Use descriptive filenames
- Keep videos under 500MB
- Delete old videos periodically
- Organize by location/date

---

### 11. Troubleshooting

#### Common Issues and Solutions

**Problem: Upload Fails**
- ✅ Check file size (max 500MB)
- ✅ Verify file format (MP4, AVI, MOV, MKV)
- ✅ Check internet connection
- ✅ Try refreshing the page

**Problem: Processing Takes Too Long**
- ✅ Large videos need more time
- ✅ Wait at least 10-15 minutes
- ✅ Check processing status periodically
- ✅ Contact support if exceeds 30 minutes

**Problem: No Results Shown**
- ✅ Ensure video has completed processing
- ✅ Refresh the dashboard
- ✅ Check video quality
- ✅ Try re-processing

**Problem: Cannot Login**
- ✅ Verify username and password
- ✅ Check caps lock key
- ✅ Reset password (if available)
- ✅ Create new account if needed

**Problem: Low Vehicle Count**
- ✅ Video might have low traffic
- ✅ Check video quality and clarity
- ✅ Ensure vehicles are visible
- ✅ Try different video angles

---

### 12. Keyboard Shortcuts

- `Ctrl + R`: Refresh page
- `Ctrl + W`: Close tab
- `F5`: Reload page
- `Esc`: Close modal/dialog

---

### 13. Privacy and Security

#### Your Data
- Videos are stored securely on the server
- Only you can access your uploaded videos
- Results are private to your account
- Passwords are encrypted

#### Security Tips
- Use strong passwords
- Don't share your login credentials
- Logout when using public computers
- Keep your account information updated

---

### 14. System Limitations

#### Current Limitations
- Maximum video size: 500MB
- Supported formats: MP4, AVI, MOV, MKV
- One video processing at a time recommended
- Results available for 90 days (may vary)

#### Vehicle Detection Limitations
- Heavily obscured vehicles may not be detected
- Very small vehicles in distance may be missed
- Similar-looking vehicles may be misclassified
- Extreme weather conditions affect accuracy

---

### 15. Getting Help

#### Support Resources

**Technical Issues**
- Check this user manual
- Review DOCUMENTATION.md
- Contact system administrator
- Email: support@example.com

**Feature Requests**
- Suggest new features
- Report bugs
- Provide feedback

---

### 16. Tips for Advanced Users

#### Optimizing Results
- Upload multiple videos from same location
- Compare results across different times
- Track traffic patterns over time
- Use results for traffic planning

#### Data Analysis
- Export results (future feature)
- Compare different locations
- Identify peak traffic times
- Analyze vehicle type distribution

---

### 17. Frequently Asked Questions (FAQ)

**Q: How long does video processing take?**
A: Typically 2-10 minutes depending on video length. Longer videos may take up to 30 minutes.

**Q: Can I process multiple videos simultaneously?**
A: One video at a time is recommended for optimal performance.

**Q: What if my video format is not supported?**
A: Convert your video to MP4 using free tools like VLC or HandBrake.

**Q: Are my videos shared with others?**
A: No, your videos and results are private to your account only.

**Q: Can I download the processed video?**
A: This feature may be available in future updates.

**Q: What happens if processing fails?**
A: You can try re-processing or upload a different video. Check video quality.

**Q: How accurate is the vehicle detection?**
A: Typically 85-95% accurate with good quality videos.

**Q: Can I delete uploaded videos?**
A: Video deletion feature coming in future update.

---

### 18. Updates and New Features

#### Recent Updates
- Version 1.0: Initial release
- User authentication system
- YOLOv8 integration
- Interactive dashboard
- Chart visualizations

#### Upcoming Features
- Real-time video processing
- Mobile app
- PDF report generation
- Video deletion
- User profile management
- Email notifications
- Advanced analytics

---

### 19. Glossary

- **AI (Artificial Intelligence)**: Computer systems that perform tasks requiring human intelligence
- **YOLO**: You Only Look Once - a fast object detection algorithm
- **Dashboard**: Main control panel after login
- **Processing**: Converting video to vehicle count data
- **Frame**: Single image from a video
- **Detection**: Identifying vehicles in images
- **Classification**: Categorizing vehicle types

---

### 20. Contact Information

For any questions, issues, or feedback:

- **Email**: support@traffic-detection.com
- **Website**: www.traffic-detection.com
- **Documentation**: See README.md and DOCUMENTATION.md files

---

## Quick Reference Card

| Task | Action |
|------|--------|
| Register | Click "Register here" on login page |
| Login | Enter username and password |
| Upload Video | Click "Select Traffic Video" → Choose file → Upload |
| Process Video | Find video → Click "Process" button |
| View Results | Click "View" on completed video |
| Logout | Click "Logout" in navigation bar |

---

**Thank you for using the Traffic Vehicle Detection System!**

*Version 1.0 - Last Updated: 2024*
