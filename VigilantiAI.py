import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyttsx3
import time
import threading
import os

# MediaPipe and Audio Setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                   refine_landmarks=True, min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)
engine = pyttsx3.init()

def speak(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait()), daemon=True).start()

# Constants
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]
MOUTH = [61, 291, 13, 14]

EAR_THRESHOLD = 0.20
EAR_CONSEC_FRAMES = 30
MAR_OPEN = 0.6
MAR_CLOSE = 0.4
COOLDOWN = 1.5

# State Variables
counter = 0
yawn_count = 0
mouth_state = "closed"
last_yawn_time = 0
detection_running = False
alert_playing = False
alarm_active = False

ear_values, mar_values = [], []

# UI Setup
root = tk.Tk()
root.title("Driver Drowsiness and Yawn Detection")
root.configure(bg="#121212")

# Dynamic layout update
def update_layout(event=None):
    width, height = root.winfo_width(), root.winfo_height()
    part_h = (height - 60) // 2
    part_w = width // 2

    frame_drowsy.place(x=0, y=0, width=part_w, height=part_h)
    frame_yawn.place(x=0, y=part_h, width=part_w, height=part_h)
    log_text.place(x=part_w, y=part_h, width=part_w, height=part_h)
    canvas.get_tk_widget().place(x=part_w, y=0, width=part_w, height=part_h)
    button_frame.place(x=0, y=height - 60, width=width, height=60)

# Frames
frame_drowsy = tk.Label(root, bg="black")
frame_yawn = tk.Label(root, bg="black")
log_text = tk.Text(root, bg="#1e1e1e", fg="white", font=("Consolas", 10), state=tk.DISABLED)

def log_message(msg):
    timestamp = time.strftime("%H:%M:%S")
    log_text.configure(state=tk.NORMAL)
    log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
    log_text.configure(state=tk.DISABLED)
    log_text.see(tk.END)

# Graphs
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 3), dpi=100)
fig.subplots_adjust(hspace=0.5)
ax1.set_title("EAR (Eye Aspect Ratio)")
ax2.set_title("MAR (Mouth Aspect Ratio)")
ax1.set_ylim(0, 0.4)
ax2.set_ylim(0, 1.0)
line1, = ax1.plot([], [], color='cyan')
line2, = ax2.plot([], [], color='magenta')
canvas = FigureCanvasTkAgg(fig, master=root)

def update_graphs():
    line1.set_data(range(len(ear_values)), ear_values)
    line2.set_data(range(len(mar_values)), mar_values)
    ax1.set_xlim(max(0, len(ear_values) - 100), len(ear_values))
    ax2.set_xlim(max(0, len(mar_values) - 100), len(mar_values))
    canvas.draw()

# Buttons
button_frame = tk.Frame(root, bg="#121212")

def clear_logs():
    log_text.configure(state=tk.NORMAL)
    log_text.delete("1.0", tk.END)
    log_text.configure(state=tk.DISABLED)

def save_logs():
    logs = log_text.get("1.0", tk.END)
    if logs.strip() == "":
        messagebox.showinfo("Save Logs", "No logs to save!")
        return
    try:
        os.makedirs("logs", exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join("logs", f"log-{timestamp}.txt")
        with open(filename, "w") as f:
            f.write("==== Detection Logs ====\n")
            f.write(logs)
            f.write("\n==== EAR Values ====\n")
            f.write('\n'.join(map(str, ear_values)))
            f.write("\n\n==== MAR Values ====\n")
            f.write('\n'.join(map(str, mar_values)))
            f.write("\n\n==== Summary ====\n")
            f.write(f"Total Yawns Detected: {yawn_count}\n")
            f.write(f"Total Drowsiness Events: {sum(1 for line in logs.splitlines() if 'Drowsiness Detected' in line)}\n")
        messagebox.showinfo("Save Logs", f"All data saved to:\n{filename}")
    except Exception as e:
        messagebox.showerror("Save Logs", f"Failed to save log file:\n{e}")

def start_detection():
    global detection_running
    if not detection_running:
        detection_running = True
        log_message("Detection started.")
        threading.Thread(target=update_frames, daemon=True).start()

def stop_detection():
    global detection_running, alert_playing, alarm_active
    detection_running = False
    alert_playing = False
    alarm_active = False
    log_message("Detection stopped.")

for text, color, cmd in [
    ("Start", "#28a745", start_detection),
    ("Stop", "#dc3545", stop_detection),
    ("Clear Logs", "#007bff", clear_logs),
    ("Save Logs", "#17a2b8", save_logs),
    ("Exit", "#6c757d", root.quit)
]:
    tk.Button(button_frame, text=text, font=("Arial", 12), bg=color, fg="white",
              command=cmd).pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='x')

# Detection Logic
cap = cv2.VideoCapture(0)

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_EAR(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def alarm_sound():
    while alarm_active:
        speak("Drowsiness detected! Wake up!")
        time.sleep(2)

def update_frames():
    global counter, yawn_count, alert_playing, alarm_active, mouth_state, last_yawn_time

    while detection_running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(frame_rgb)

        drowsy_frame = frame.copy()
        yawn_frame = frame.copy()

        h, w = frame.shape[:2]

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark
            def get_point(idx):
                return np.array([landmarks[idx].x * w, landmarks[idx].y * h])

            left_eye = [get_point(i) for i in LEFT_EYE]
            right_eye = [get_point(i) for i in RIGHT_EYE]
            ear = (calculate_EAR(left_eye) + calculate_EAR(right_eye)) / 2.0
            ear_values.append(ear)

            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= EAR_CONSEC_FRAMES and not alert_playing:
                    log_message("Drowsiness Detected")
                    alert_playing = True
                    alarm_active = True
                    threading.Thread(target=alarm_sound, daemon=True).start()
            else:
                counter = 0
                alert_playing = False
                alarm_active = False

            for point in left_eye + right_eye:
                cv2.circle(drowsy_frame, tuple(point.astype(int)), 2, (0, 255, 0), -1)

            mar = euclidean(get_point(MOUTH[2]), get_point(MOUTH[3])) / \
                  euclidean(get_point(MOUTH[0]), get_point(MOUTH[1]))
            mar_values.append(mar)

            if mouth_state == "closed" and mar > MAR_OPEN:
                mouth_state = "open"
            elif mouth_state == "open" and mar < MAR_CLOSE:
                if time.time() - last_yawn_time > COOLDOWN:
                    yawn_count += 1
                    log_message(f"Yawn #{yawn_count} Detected")
                    if yawn_count % 5 == 0:
                        speak("Too many yawns, take a break!")
                        log_message("Too many yawns, take a break!")
                    else:
                        speak("Yawn Detected")
                    last_yawn_time = time.time()
                mouth_state = "closed"

            mp.solutions.drawing_utils.draw_landmarks(
                image=yawn_frame,
                landmark_list=result.multi_face_landmarks[0],
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1)
            )
        else:
            log_message("No face detected")

        d_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(drowsy_frame, cv2.COLOR_BGR2RGB)))
        frame_drowsy.configure(image=d_img)
        frame_drowsy.image = d_img

        y_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(yawn_frame, cv2.COLOR_BGR2RGB)))
        frame_yawn.configure(image=y_img)
        frame_yawn.image = y_img

        update_graphs()
        time.sleep(0.03)

def on_closing():
    global detection_running, alarm_active
    detection_running = False
    alarm_active = False
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Configure>", update_layout)
root.mainloop()
