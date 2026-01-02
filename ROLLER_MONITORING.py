import cv2
import time
import numpy as np
import winsound

# ---------------- PARAMETERS ----------------
TIME_LIMIT = 8  # seconds
PAINT_PIXEL_THRESHOLD = 500
alarm_active = False

# Paint color HSV (adjust if needed)
LOWER_COLOR = np.array([20, 100, 100])
UPPER_COLOR = np.array([30, 255, 255])

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

top_detect_time = None
bottom_detected = False

print("🎥 Roller Monitoring Started | Press ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # -------- Define TOP & BOTTOM zones --------
    top_zone = frame[0:int(h*0.3), :]
    bottom_zone = frame[int(h*0.7):h, :]

    # Convert to HSV
    hsv_top = cv2.cvtColor(top_zone, cv2.COLOR_BGR2HSV)
    hsv_bottom = cv2.cvtColor(bottom_zone, cv2.COLOR_BGR2HSV)

    mask_top = cv2.inRange(hsv_top, LOWER_COLOR, UPPER_COLOR)
    mask_bottom = cv2.inRange(hsv_bottom, LOWER_COLOR, UPPER_COLOR)

    top_pixels = cv2.countNonZero(mask_top)
    bottom_pixels = cv2.countNonZero(mask_bottom)

    current_time = time.time()

    # -------- TOP paint detected --------
    if top_pixels > PAINT_PIXEL_THRESHOLD:
        top_detect_time = current_time
        bottom_detected = False
        alarm_active = False

    # -------- BOTTOM paint detected --------
    if top_detect_time and bottom_pixels > PAINT_PIXEL_THRESHOLD:
        bottom_detected = True
        cv2.putText(frame, "ROLLER ROTATING", (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        top_detect_time = None

    # -------- TIME CHECK --------
    if top_detect_time and not bottom_detected:
        elapsed = current_time - top_detect_time

        if elapsed > TIME_LIMIT:
            cv2.putText(frame, "ROLLER NOT ROTATING", (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if not alarm_active:
                winsound.Beep(2000, 1000)
                alarm_active = True

    # -------- Draw Zones --------
    cv2.rectangle(frame, (0, 0), (w, int(h*0.3)), (255, 0, 0), 2)
    cv2.rectangle(frame, (0, int(h*0.7)), (w, h), (0, 0, 255), 2)

    cv2.imshow("Roller Monitoring", frame)
    cv2.imshow("Top Mask", mask_top)
    cv2.imshow("Bottom Mask", mask_bottom)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
