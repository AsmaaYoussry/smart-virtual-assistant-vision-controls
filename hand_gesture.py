import mediapipe as mp
import cv2
import pyautogui
from voice_feedback import VoiceFeedbackModule  # Importing the VoiceFeedbackModule

# Initialize VoiceFeedbackModule (you can do it here or pass it as a parameter)
voice = VoiceFeedbackModule()

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Define landmark indices for finger tips
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

# For scroll detection, tracking the previous Y-position of the index finger
prev_index_y = None

def classify_gesture(landmarks):
    """
    Determines the hand gesture based on key landmark positions.
    """
    global prev_index_y

    thumb_tip = landmarks[THUMB_TIP].y
    index_tip = landmarks[INDEX_TIP].y
    middle_tip = landmarks[MIDDLE_TIP].y
    ring_tip = landmarks[RING_TIP].y
    pinky_tip = landmarks[PINKY_TIP].y

    # Detect Open Hand (all fingers extended)
    if (index_tip < landmarks[INDEX_TIP - 2].y and
        middle_tip < landmarks[MIDDLE_TIP - 2].y and
        ring_tip < landmarks[RING_TIP - 2].y and
        pinky_tip < landmarks[PINKY_TIP - 2].y and
        thumb_tip < landmarks[THUMB_TIP - 2].y):  # Ensure the thumb is also extended
        gesture = "Play/Pause"
        voice.speak("Pause")  # <-- Add feedback here
        return gesture

    # Detect Fist (all fingers curled)
    elif (index_tip > landmarks[INDEX_TIP - 2].y and
          middle_tip > landmarks[MIDDLE_TIP - 2].y and
          ring_tip > landmarks[RING_TIP - 2].y and
          pinky_tip > landmarks[PINKY_TIP - 2].y and
          thumb_tip > landmarks[THUMB_TIP - 2].y):  # Ensure the thumb is also curled
        gesture = "Mute/Unmute"
        return gesture

    # Detect Victory (index and middle fingers raised)
    elif (index_tip < landmarks[INDEX_TIP - 2].y and
          middle_tip < landmarks[MIDDLE_TIP - 2].y and
          ring_tip > landmarks[RING_TIP - 2].y and
          pinky_tip > landmarks[PINKY_TIP - 2].y and
          thumb_tip > landmarks[THUMB_TIP - 2].y):  # Ensure the thumb is curled
        gesture = "Previous (Rewind)"
        voice.speak("Going back")  # <-- Add feedback here
        return gesture

    # Detect Raise Index (only the index raised)
    elif index_tip < landmarks[INDEX_TIP - 2].y and \
         middle_tip > landmarks[MIDDLE_TIP - 2].y and \
         ring_tip > landmarks[RING_TIP - 2].y and \
         pinky_tip > landmarks[PINKY_TIP - 2].y:
        gesture = "Next (Skip)"
        voice.speak("Next")  # <-- Add feedback here
        return gesture

    # Detect Pinky Up (Only pinky finger raised)
    elif pinky_tip < landmarks[PINKY_TIP - 2].y and \
         index_tip > landmarks[INDEX_TIP - 2].y and \
         middle_tip > landmarks[MIDDLE_TIP - 2].y and \
         ring_tip > landmarks[RING_TIP - 2].y:
        gesture = "Increase Volume"
        return gesture

    # Detect Decrease Volume (index, middle, and ring fingers raised)
    elif index_tip < landmarks[INDEX_TIP - 2].y and \
         middle_tip < landmarks[MIDDLE_TIP - 2].y and \
         ring_tip < landmarks[RING_TIP - 2].y and \
         pinky_tip > landmarks[PINKY_TIP - 2].y:
        gesture = "Decrease Volume"
        return gesture

    # Detect Scrolling (based on index finger movement)
    if prev_index_y is not None:
        if index_tip < prev_index_y - 0.05:
            prev_index_y = index_tip
            gesture = "Next (Skip)"
            return gesture
        elif index_tip > prev_index_y + 0.05:
            prev_index_y = index_tip
            gesture = "Scroll Down"
            return gesture
    prev_index_y = index_tip

    return "Unknown Gesture"

# For media control (volume adjustments)
def control_volume(action):
    if action == "increase":
        pyautogui.press("volumeup")  # Simulate volume up key press
    elif action == "decrease":
        pyautogui.press("volumedown")  # Simulate volume down key press