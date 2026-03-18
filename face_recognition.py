from deepface import DeepFace
import cv2
import os
from voice_feedback import VoiceFeedbackModule  # <-- Import the VoiceFeedbackModule

# Initialize VoiceFeedbackModule (you can do it here, or you can pass the voice instance as a parameter)
voice = VoiceFeedbackModule()

# === CONFIG ===
FACE_DB_PATH = "photoss"

def authenticate_face(frame):
    try:
        # Search in folder
        result = DeepFace.find(
            img_path=frame,
            db_path=FACE_DB_PATH,
            enforce_detection=False,
            detector_backend='opencv',  # or 'mediapipe'
            model_name="VGG-Face",
            silent=True
        )

        if len(result) > 0 and len(result[0]) > 0:
            identity_path = result[0].iloc[0]['identity']
            name = os.path.basename(identity_path).split('.')[0]
            
            # Assuming user_result is a dictionary with information about the recognition
            user_result = {
                "is_authorized": True,  # Example condition, you may adjust this based on your needs
                "recognized_user": name
            }

            if user_result["is_authorized"]:
                voice.speak(f"Welcome, {user_result['recognized_user']}")
            else:
                voice.speak("Unauthorized user")
            
            return name  # return authorized name
        else:
            return None
    except Exception as e:
        print(" Face recognition error:", e)
        return None