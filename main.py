import cv2
import numpy as np
import time
import os
from face_recognition import authenticate_face
from hand_gesture import classify_gesture, control_volume
from ocr import OCRModule
import mediapipe as mp
import pyautogui
from voice_feedback import VoiceFeedbackModule  # Import the VoiceFeedbackModule

# -------- Initialize Voice Feedback --------
# -------- Initialize Voice Feedback --------
voice = VoiceFeedbackModule()  # <-- Initialize the voice feedback module
voice.speak("Hello, Smart Assistant is now running.")  # <-- Speak the startup message

# Initialize a flag to ensure "Welcome" is spoken only once
welcome_spoken = False

# -------- Load Calibration --------
try:
    data = np.load("stereo_calibration_data.npz")
    camera_matrix = data["camera_matrix_left"]
    dist_coeffs = data["dist_coeffs_left"]
    print("[✅] Loaded stereo calibration (left camera).")
except:
    camera_matrix = None
    dist_coeffs = None
    print("[⚠] Stereo calibration data not found. Running without undistortion.")

# -------- Initialize Vision Modules --------
cap = cv2.VideoCapture(0)
authenticated = False
current_name = ""

ocr = OCRModule()
ocr.set_debug(False)
roi = (300, 200, 300, 100)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

frame_count = 0
gesture_text = ""
ocr_text = ""
last_action_time = 0
cooldown = 2

print("📸 Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if camera_matrix is not None and dist_coeffs is not None:
        frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Face recognition every 30 frames
    frame_count += 1
    if frame_count % 30 == 0:
        resized = cv2.resize(frame, (300, 300))
        name = authenticate_face(resized)
        authenticated = bool(name)
        current_name = name if name else "Unknown"

        # Check if user is authenticated and speak "Welcome" only once
        if authenticated and not welcome_spoken:
            voice.speak(f"Welcome, {current_name}")
            welcome_spoken = True  # Set the flag to True to avoid speaking "Welcome" again
        elif not authenticated:
            welcome_spoken = False  # Reset the flag if user is not authenticated anymore

    # OCR
    ocr_text = ocr.extract_text(frame, roi)
    frame = ocr.draw_roi(frame, roi)

    # Gesture Detection
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture_text = classify_gesture(hand_landmarks.landmark)

            if authenticated and (time.time() - last_action_time > cooldown):
                if gesture_text == "Play/Pause":
                    pyautogui.press("playpause")
                elif gesture_text == "Mute/Unmute":
                    pyautogui.press("volumemute")
                elif gesture_text == "Next (Skip)":
                    pyautogui.press("right")
                elif gesture_text == "Previous (Rewind)":
                    pyautogui.press("left")
                elif gesture_text == "Increase Volume":
                    control_volume("increase")
                elif gesture_text == "Decrease Volume":
                    control_volume("decrease")
                last_action_time = time.time()

    # UI Feedback
    label = f"User: {current_name}" if authenticated else "Unauthorized"
    cv2.putText(frame, label, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (0, 255, 0) if authenticated else (0, 0, 255), 2)
    cv2.putText(frame, f"OCR: {ocr_text[:30]}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, f"Gesture: {gesture_text}", (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 100, 255), 2)

    cv2.imshow("Smart Assistant", frame)

    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
        break

cap.release()
cv2.destroyAllWindows()