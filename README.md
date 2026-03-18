# 🤖 Smart Virtual Assistant with Vision-Based Controls

## 📌 Overview
This project presents a vision-based desktop virtual assistant capable of performing tasks using hand gestures and facial recognition. The system enables hands-free interaction by combining computer vision, OCR, and real-time feedback to control applications and extract information.

---

## 🎯 Objective
To design and implement an intelligent assistant that:
- Recognizes predefined hand gestures for system control  
- Identifies users through face recognition  
- Extracts text from physical documents using OCR  
- Provides real-time visual feedback  

---

## 🚀 Core Functionalities

### 1. 👤 User Authentication
- Implemented face recognition using **MediaPipe / DeepFace**
- Authorized users can activate gesture-based controls

### 2. ✋ Gesture-Based Control
- Real-time hand tracking using **OpenCV + MediaPipe**
- Recognized multiple gestures to:
  - Control media playback  
  - Adjust volume  
  - Navigate content  

### 3. 📄 OCR Module
- Captured regions of interest from camera input  
- Extracted text using **Tesseract OCR**

### 4. 📺 Live Feedback System
- Displayed:
  - User identity  
  - Recognition status  
  - OCR output  
- Provided real-time on-screen feedback

### 5. 🎯 Camera Calibration
- Used **OpenCV calibration techniques**  
- Improved detection accuracy using intrinsic/extrinsic parameters  

---

## ⭐ Bonus Features
- 🔊 Text-to-speech feedback  
- 👥 Multi-user support  
- 🎨 Gesture-controlled drawing (paint canvas)  

---

## 🧠 Technologies Used
- Python  
- OpenCV  
- MediaPipe  
- DeepFace  
- Tesseract OCR  
- NumPy  

---

## 👥 Contribution
This project was developed as part of a team.


