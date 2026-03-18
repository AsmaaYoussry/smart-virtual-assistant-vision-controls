import pyttsx3

class VoiceFeedbackModule:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)      # Speed of speech
        self.engine.setProperty('volume', 1.0)    # Volume: 0.0 to 1.0

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
        