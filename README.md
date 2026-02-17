
# 🚗 SafeDrive – Driver Drowsiness Detection System

SafeDrive is a real-time driver safety application designed to prevent accidents caused by driver fatigue. It uses computer vision and facial landmark detection to monitor the driver's state (drowsiness and yawning) and issues timely visual and audio alerts.

---

## ⚙️ Key Features

- **Real-Time Monitoring**: Uses a webcam to track facial landmarks in real-time with **MediaPipe** and **OpenCV**.
- **Drowsiness Detection**: Calculates the Eye Aspect Ratio (EAR) to detect prolonged eye closure.
- **Yawn Detection**: Calculates the Mouth Aspect Ratio (MAR) to detect yawning frequency.
- **Visual & Audio Alerts**: triggers an alarm sound and visual warning when fatigue is detected.
- **Interactive GUI**: A user-friendly interface built with **Tkinter** to start/stop detection, clear logs, and view live graphs.
- **Live Data Visualization**: Real-time plotting of EAR and MAR values using **Matplotlib**.
- **Session Logging**: Automatically saves detection logs and data to the `logs/` directory for review.

---

## 🔧 Tech Stack

- **Python 3.11+**
- **OpenCV**: For video capture and image processing.
- **MediaPipe**: For high-fidelity face mesh detection.
- **Tkinter**: For building the desktop GUI application.
- **Matplotlib**: For plotting real-time EAR and MAR graphs.
- **Pyttsx3**: For text-to-speech audio alerts.
- **NumPy & Pillow**: For numerical operations and image handling.

---

## 🧩 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/vivekvarma-01/Safe-Drive.git
   cd Safe-Drive
   ```

2. **Install Dependencies**
   Ensure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### Option 1: Run via Batch Script (Windows)
Double-click `start.bat` or run it from the command line:
```bash
start.bat
```
This script automatically checks for the Python launcher and runs the application.

### Option 2: Run via Python
Directly execute the main script:
```bash
python SafeDrive.py
```

### Operational Steps:
1.  Click **"Start"** to begin monitoring.
2.  The application will track your eye blinks and mouth movements.
3.  **Alerts**:
    *   **Drowsiness**: Triggered if eyes remain closed for a specific duration.
    *   **Yawning**: Triggered if the mouth opens wide beyond a threshold.
    *   **Excessive Yawning**: Warning issued after multiple yawns in a short period.
4.  Real-time graphs updating below the camera feed show your EAR and MAR values.
5.  Click **"Stop"** to end the session.
6.  Click **"Save Logs"** to export the session data to the `logs/` folder.

---

## 🧠 How It Works

1.  **Face Mesh**: Creates a 468-point 3D face mesh from the webcam feed.
2.  **EAR Calculation**: Measures the ratio of eye height to eye width to determine if eyes are open or closed.
3.  **MAR Calculation**: Measures the ratio of mouth height to mouth width to detect yawning.
4.  **Threshold Logic**:
    *   `EAR < 0.20`: Eyes considered closed.
    *   `MAR > 0.6`: Mouth considered open (yawning).
5.  **Alert System**: If thresholds are crossed for a set number of consecutive frames, audio and visual alarms are triggered.

---

## 📂 Project Structure

```
├── logs/                 # Stores session logs (timestamped text files)
├── SafeDrive.py          # Main application script
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── start.bat             # Quick launch script for Windows
```

---

## 📌 Future Enhancements

- [ ] Integrate deep learning models for more robust fatigue detection.
- [ ] Add support for head pose estimation (distraction detection).
- [ ] Mobile app integration.
- [ ] refined threshold tuning UI.
