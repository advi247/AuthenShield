import cv2
import mediapipe as mp
import numpy as np
import time
from pynput import mouse
import threading

# ========== Face Mesh Setup ==========
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def calculate_ear(eye_landmarks):
    vertical1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
    vertical2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
    horizontal = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

# ========== Mouse Movement Tracker ==========
mouse_moves = [0]
def on_move(x, y):
    mouse_moves[0] += 1

mouse_listener = mouse.Listener(on_move=on_move)
mouse_listener.start()

# ========== Camera & EAR Detection ==========
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ear_values = []
start_time = time.time()
DETECTION_DURATION = 10  # seconds

print("[INFO] Starting detection...")

while time.time() - start_time < DETECTION_DURATION:
    success, frame = cap.read()
    if not success:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            left_eye = np.array([(int(face_landmarks.landmark[i].x * w),
                                  int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE], dtype=np.float32)
            right_eye = np.array([(int(face_landmarks.landmark[i].x * w),
                                   int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE], dtype=np.float32)

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            ear_values.append(avg_ear)
            cv2.putText(frame, f'EAR: {avg_ear:.2f}', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Eye Blink Detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
mouse_listener.stop()

# ========== Final Decision ==========
avg_ear = np.mean(ear_values) if ear_values else 0
mouse_activity = mouse_moves[0]

print("\n[SUMMARY]")
print(f"- Avg EAR: {avg_ear:.2f}")
print(f"- Mouse Movements: {mouse_activity}")

# Decision Logic
if not ear_values or mouse_activity < 3:
    print("\n[RESULT] Bot Detected ")
else:
    print("\n[RESULT] Human Detected")

