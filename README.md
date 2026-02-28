# Drowsiness Detection in Drivers 🚗💤

An AI-powered safety system designed to prevent road accidents by monitoring driver fatigue in real-time. Built with Python, OpenCV, and Dlib.

## 🚀 Overview
This system uses a 68-point facial landmark model to analyze a driver's face. Unlike basic systems, this version includes specific logic to avoid false alarms (like laughing or long blinks) and focuses on actual drowsiness indicators.



## ✨ Key Features
- **Smart EAR (Eye Aspect Ratio):** Only triggers an alarm if eyes are closed for more than **3 continuous seconds**.
- **Yawn Detection (MAR):** Monitors Mouth Aspect Ratio to detect yawning, a primary sign of fatigue.
- **Neon HUD Dashboard:** A professional dark-mode UI with live telemetry charts.
- **Audio Alerts:** Instant siren alarm when critical drowsiness is detected.

## 🧠 The Math Behind the Safety
The system calculates two main metrics:

1. **EAR (Eye Aspect Ratio):**
   - Threshold: `0.22`
   - Trigger: `60 consecutive frames (~3 seconds)`
   - *Prevents false triggers from squinting or laughing.*

2. **MAR (Mouth Aspect Ratio):**
   - Threshold: `0.5`
   - Trigger: `20 consecutive frames`
   - *Detects deep yawns regardless of eye status.*



## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/mottesomeshwar/Drowsiness-Detection-System.git](https://github.com/mottesomeshwar/Drowsiness-Detection-System.git)









