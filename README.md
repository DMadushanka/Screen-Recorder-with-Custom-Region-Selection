Screen Recorder with Custom Region Selection
This Python application is a screen recording tool that allows users to record their screen with options to select a custom recording region, apply rounded corners to the recording, and save the output as an MP4 file. The application provides an intuitive GUI built with tkinter and integrates with matplotlib for visualizing and selecting the recording area.

Features:
Custom Region Selection: Use a graphical interface to draw and select the area of the screen to record.
Full-Screen Recording: Default to full-screen recording if no custom region is selected.
Rounded Corners: Apply rounded corners to the recorded video for a polished look.
Save Location: Choose a directory to save the recorded video.
Real-Time Recording: Capture the screen in real-time and save the output as an MP4 file.
Intuitive GUI: User-friendly interface for starting, stopping, and configuring recordings.
Technologies Used:
Python Libraries:
tkinter: For the graphical user interface.
pyautogui: For capturing screenshots of the screen.
cv2 (OpenCV): For video processing and saving the recording.
numpy: For creating masks with rounded corners.
matplotlib: For visualizing and selecting the recording area.
threading: For running the recording process in a separate thread.
Video Codec: Uses the X264 codec to save recordings in MP4 format.
Requirements:
Operating System: Windows (recommended) or other platforms supporting the required libraries.
Python Version: 3.8 or higher
Dependencies:
pyautogui
opencv-python
numpy
matplotlib
How to Use:
Select Save Location: Click the "Browse Save Location" button to choose where the recording will be saved.
Draw Recording Area:
Click "Draw Recording Area" to open a fullscreen overlay.
Use the mouse to draw a rectangle representing the recording area.
Press "Enter" to save the selected area.
Start Recording: Click "Start Recording" to begin capturing the screen.
Stop Recording: Click "Stop Recording" to end the recording and save the video.
Full-Screen Recording: If no area is selected, the application will record the entire screen.
Disclaimer:
This application is designed for educational and personal use. Ensure you have permission to record any content before using this tool.

You can copy and paste this into your GitHub repository's README.md file or the description section.
