import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize variables
curl_count = 0
curl_stage = None
progress = 0

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def draw_vertical_progress_bar(image, progress, width, height):
    bar_width = int(width * 0.03)
    bar_height = int(height * 0.6)
    start_x = int(width * 0.95)
    start_y = int((height - bar_height) / 2)
    
    # Draw background
    cv2.rectangle(image, (start_x, start_y), (start_x + bar_width, start_y + bar_height), (200, 200, 200), -1)
    
    # Draw progress
    filled_height = int((progress / 100) * bar_height)
    cv2.rectangle(image, (start_x, start_y + bar_height - filled_height), 
                  (start_x + bar_width, start_y + bar_height), (0, 255, 0), -1)
    
    # Draw percentage text
    cv2.putText(image, f"{int(progress)}%", (start_x - 50, start_y + bar_height + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def draw_text_with_shadow(image, text, position, font_scale, font_color, font_thickness, shadow_color=(0, 0, 0)):
    """Draws text with a shadow to enhance the stylish effect."""
    # Draw shadow (offset by a few pixels)
    offset_position = (position[0] + 2, position[1] + 2)
    cv2.putText(image, text, offset_position, cv2.FONT_HERSHEY_COMPLEX, font_scale, shadow_color, font_thickness + 2, cv2.LINE_AA)
    
    # Draw main text
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_COMPLEX, font_scale, font_color, font_thickness, cv2.LINE_AA)

cap = cv2.VideoCapture(0)

# Get full screen dimensions
cv2.namedWindow('Bicep Curl Counter', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Bicep Curl Counter', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to full screen
    frame = cv2.resize(frame, (screen_width, screen_height))

    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        # Calculate angle
        angle = calculate_angle(shoulder, elbow, wrist)

        # Curl counter logic
        if angle > 160:
            if curl_stage == "up":
                curl_count += 1
            curl_stage = "down"
            progress = 0
        elif angle < 30:
            curl_stage = "up"
            progress = 100
        else:
            progress = max(0, min(100, (160 - angle) / 1.3))

        # Visualize curls and stage with improved positioning and shadowed text
        text_color = (0, 255, 255)  # Bright yellow color
        shadow_color = (0, 0, 0)    # Black shadow for stylish effect
        font_scale_curls = 1.5  # Reduced font size for curls
        font_scale_stage = 1.2  # Reduced font size for stage
        font_thickness = 2

        # Place curls in the top-left corner
        draw_text_with_shadow(image, f"Curls: {curl_count}", (int(screen_width * 0.05), int(screen_height * 0.1)), 
                              font_scale_curls, text_color, font_thickness, shadow_color)

        # Place stage in the bottom-left corner
        draw_text_with_shadow(image, f"Stage: {curl_stage}", (int(screen_width * 0.05), int(screen_height * 0.9)), 
                              font_scale_stage, text_color, font_thickness, shadow_color)

        # Draw progress bar (no changes to this)
        draw_vertical_progress_bar(image, progress, screen_width, screen_height)

        # Draw pose landmarks
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

        # Highlight specific landmarks
        landmarks_to_highlight = [
            mp_pose.PoseLandmark.NOSE,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.RIGHT_ELBOW,
            mp_pose.PoseLandmark.RIGHT_WRIST
        ]
        for landmark in landmarks_to_highlight:
            lm = landmarks[landmark.value]
            cv2.circle(image, (int(lm.x * screen_width), int(lm.y * screen_height)), 5, (0, 255, 0), -1)

    except Exception as e:
        print(f"An error occurred: {e}")

    cv2.imshow('Bicep Curl Counter', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()