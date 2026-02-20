// Dashboard specific JavaScript

// Upload Form Handler
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('videoFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select a video file!', 'warning');
        return;
    }
    
    // Validate file size (500MB max)
    const maxSize = 500 * 1024 * 1024; // 500MB in bytes
    if (file.size > maxSize) {
        showAlert('File size exceeds 500MB limit!', 'danger');
        return;
    }
    
    // Show progress
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = uploadProgress.querySelector('.progress-bar');
    
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
    uploadProgress.style.display = 'block';
    
    // Create form data
    const formData = new FormData();
    formData.append('video', file);
    
    try {
        // Upload video
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Video uploaded successfully! You can now process it.', 'success');
            
            // Reset form
            document.getElementById('uploadForm').reset();
            document.getElementById('videoPreview').style.display = 'none';
            
            // Reload page after 2 seconds to show new video
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showAlert('Upload failed: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showAlert('Upload error: ' + error.message, 'danger');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-upload"></i> Upload Video';
        uploadProgress.style.display = 'none';
        progressBar.style.width = '0%';
    }
});

// Process Video Buttons
document.querySelectorAll('.process-btn').forEach(button => {
    button.addEventListener('click', async function() {
        const videoId = this.getAttribute('data-video-id');
        
        if (!confirmAction('Start processing this video? This may take several minutes.')) {
            return;
        }
        
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';
        
        try {
            const response = await fetch(`/process/${videoId}`, {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                showAlert('Processing started! The page will update when complete.', 'info');
                
                // Update button
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing';
                this.classList.remove('btn-primary');
                this.classList.add('btn-warning');
                
                // Start polling for status
                pollProcessingStatus(videoId);
            } else {
                showAlert('Failed to start processing: ' + result.message, 'danger');
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-play"></i> Process';
            }
        } catch (error) {
            console.error('Processing error:', error);
            showAlert('Processing error: ' + error.message, 'danger');
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-play"></i> Process';
        }
    });
});

// Poll processing status
function pollProcessingStatus(videoId) {
    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${videoId}`);
            const status = await response.json();
            
            console.log('Status Poll:', status);
            
            // Find the button for this video
            const processBtn = document.querySelector(`.process-btn[data-video-id="${videoId}"]`);
            
            if (status.status === 'completed') {
                clearInterval(pollInterval);
                if (processBtn) {
                    processBtn.innerHTML = '<i class="fas fa-check"></i> Completed';
                    processBtn.classList.remove('btn-warning');
                    processBtn.classList.add('btn-success');
                }
                showAlert('Processing completed! You can now view the results.', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else if (status.status === 'failed') {
                clearInterval(pollInterval);
                if (processBtn) {
                    processBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Failed';
                    processBtn.classList.remove('btn-warning', 'btn-primary');
                    processBtn.classList.add('btn-danger');
                }
                showAlert('Processing failed: ' + (status.error || 'Check server logs'), 'danger');
            } else if (status.status === 'processing') {
                if (processBtn) {
                    processBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Processing (${status.progress || 0}%)`;
                }
            }
        } catch (error) {
            console.error('Status poll error:', error);
        }
    }, 3000); // Poll every 3 seconds for better responsiveness
    
    // Stop polling after 30 minutes
    setTimeout(() => {
        clearInterval(pollInterval);
    }, 30 * 60 * 1000);
}

// Auto-refresh for processing videos on page load
document.addEventListener('DOMContentLoaded', function() {
    const processingVideos = document.querySelectorAll('.btn-warning[disabled]');
    
    processingVideos.forEach(button => {
        const row = button.closest('tr');
        const videoId = button.closest('td').previousElementSibling
                            .previousElementSibling
                            .previousElementSibling
                            .previousElementSibling
                            .previousElementSibling.textContent.trim();
        
        // Extract video ID from row (this is a simple approach, adjust based on your table structure)
        const allProcessBtns = document.querySelectorAll('.process-btn');
        allProcessBtns.forEach(btn => {
            if (btn.closest('tr') === row) {
                const id = btn.getAttribute('data-video-id');
                if (id) {
                    pollProcessingStatus(id);
                }
            }
        });
    });
});

// File input validation
document.getElementById('videoFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    
    if (file) {
        const fileSize = formatFileSize(file.size);
        const fileName = file.name;
        
        console.log(`File selected: ${fileName} (${fileSize})`);
        
        // Show file info
        const fileInfo = document.createElement('small');
        fileInfo.className = 'text-muted d-block mt-1';
        fileInfo.textContent = `Selected: ${fileName} (${fileSize})`;
        
        const existingInfo = this.parentElement.querySelector('small.text-muted');
        if (existingInfo && existingInfo.textContent.startsWith('Selected:')) {
            existingInfo.remove();
        }
        
        this.parentElement.appendChild(fileInfo);
    }
});
