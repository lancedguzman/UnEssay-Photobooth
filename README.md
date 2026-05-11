# 📸 Choomtie Booth
A web-based photobooth application built with Django that captures memories in a classic vintage style. Users can create photo strips or animated GIFs, personalize them with messages, and share them instantly via QR code or download.

## ✨ Features
1. Photo Mode (1x3 Collage)
- Automated Capture: Takes 3 photos in sequence with a countdown and flash effect.
- Smart Stitching: Automatically combines the 3 photos into a vertical photo strip.
- Individual Retakes: Review your shots and retake specific photos without restarting the whole session.

2. GIF Mode
- Motion Capture: Records a short burst of frames to create a looping animated GIF.
- Captioning: Add a custom text caption directly onto the GIF frames.

3. Review & Personalize
- Live Review: Check your photos or GIF before finalizing.
- Custom Messages: Add a personal note or footer text to your final photo strip.

4. Share & Save
- Direct Download: Save the final image/GIF directly to your device.
- QR Code Scan: Generates a unique QR code for users to scan and save on their phones instantly.
- Link Sharing: Copy a direct link to share with friends.

5. Responsive Design
- Optimized for Desktop, Tablets (iPad), and Mobile (iPhone).
- Fluid camera interface that adapts to portrait or landscape orientations without stretching.

## 🛠️ Tech Stack
- Backend: Python, Django 5+
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Styling: Custom CSS with a Vintage/Polaroid theme (Fonts: Cormorant Garamond & Sacramento).
- Database: SQLite (Default)

## 📂 Project Structure
``` 
photobooth/: Main app logic (Landing, Review, Result, Finalizing).
photo_capture/: Handles webcam logic for the 3-photo collage.
gif_capture/: Handles webcam logic for GIF creation.
media_processing/: Helper scripts to stitch images and burn text.
templates/: HTML files for UI (including custom 404/500 error pages).
```
