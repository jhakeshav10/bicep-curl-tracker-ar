# Bicep Curl Counter

## Overview
The Bicep Curl Counter is an interactive fitness application that utilizes computer vision and augmented reality (AR) techniques to count bicep curls in real-time. By employing MediaPipe for pose detection and OpenCV for image processing, the application provides immediate feedback on the user's exercise performance. The integration of AR enhances the user experience by overlaying essential data directly onto the video feed, creating an immersive workout environment.

### Features
- **Real-time Tracking**: Accurate detection of bicep curls using pose estimation.
- **Augmented Reality Elements**: Overlay of workout metrics (curl count and stage) on the video feed.
- **Visual Feedback**: Progress bar indicating the completion of the exercise.
- **Stylish Text Display**: Enhanced visibility with shadow effects on displayed text.
- **Fullscreen Mode**: Maximizes user engagement during workouts.

## Getting Started

### Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv myenv
3. **Activate the virtual environment:**

- On Windows:
   ```bash
   myenv\Scripts\activate
   ```
- On macOS/Linux:
   ```bash
   source myenv/bin/activate
4. **Install required packages:**

   ```bash
   pip install -r requirements.txt

### Running the Application
To run the Bicep Curl Counter, execute the following command:

```bash
python main.py
```
### Controls
- Press q to exit the application.
## Code Explanation
### Key Components
- Pose Detection: The application uses MediaPipe's Pose module to detect and track body landmarks, specifically the shoulder, elbow, and wrist.
- Curl Counting Logic: The angle between the shoulder, elbow, and wrist is calculated to determine the curl stage (up or down) and increment the curl count accordingly.
- Augmented Reality Visualization: The application overlays metrics directly onto the camera feed, allowing users to view their progress without distraction.
- OpenCV for Visualization: OpenCV is used to draw the detected landmarks, curl count, stage, and progress bar on the video feed.
### Customization
You can modify various aspects of the application, such as:

- Text colors and sizes for the display.
- Detection confidence thresholds in the mp_pose.Pose initialization.
- Adjustments to the layout and positioning of AR elements.
