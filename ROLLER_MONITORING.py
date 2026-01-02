import cv2
import time
import numpy as np
import winsound
import smtplib

# ---------------- MAIL FUNCTION ----------------
def send_alert_mail(zone_name):
    sender = "yourmail@gmail.com"
    password = "your_app_password"
    receiver = "receiver@gmail.com"

    message = f"""Subject: ROLLER STOP ALERT - {zone_name}

Paint line in {zone_name} did not reappear within 8 seconds.
Roller may have stopped.
"""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, message)
    server.quit()

# ---------------- SETTINGS ----------------
CAMERA_INDEX = 0
TIME_LIMIT = 8  # seconds
PAINT_MIN_PIXELS = 500

LOWER_COLOR = np.array([20, 100, 100])  # adjust HSV for your paint
UPPER_COLOR = np.array([30, 255, 255])

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Split zones
upper_zone = (0, 0, frame_width, frame_height // 2)  # x1,y1,x2,y2
lower_zone = (0, frame_height // 2, frame_width, frame_height)

# Initialize timers & alarm flags
last_paint_upper = time.time()
last_paint_lower = time.time()
ALARM_UPPER = False
ALARM_LOWER = False

print("Monitoring started. Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    current_time = time.time()

    # -------- Upper Zone --------
    x1, y1, x2, y2 = upper_zone
    upper_frame = frame[y1:y2, x1:x2]
    mask_upper = cv2.inRange(cv2.cvtColor(upper_frame, cv2.COLOR_BGR2HSV), LOWER_COLOR, UPPER_COLOR)
    paint_pixels_upper = cv2.countNonZero(mask_upper)

    if paint_pixels_upper > PAINT_MIN_PIXELS:
        last_paint_upper = current_time
        if ALARM_UPPER:
            print("✅ Upper Zone: Roller running again. Alarm reset.")
            ALARM_UPPER = False
        cv2.putText(frame, "Upper Zone: RUNNING", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        if current_time - last_paint_upper > TIME_LIMIT and not ALARM_UPPER:
            cv2.putText(frame, "Upper Zone: STOPPED", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            winsound.Beep(2000, 1000)
            send_alert_mail("Upper Zone")
            ALARM_UPPER = True

    # -------- Lower Zone --------
    x1, y1, x2, y2 = lower_zone
    lower_frame = frame[y1:y2, x1:x2]
    mask_lower = cv2.inRange(cv2.cvtColor(lower_frame, cv2.COLOR_BGR2HSV), LOWER_COLOR, UPPER_COLOR)
    paint_pixels_lower = cv2.countNonZero(mask_lower)

    if paint_pixels_lower > PAINT_MIN_PIXELS:
        last_paint_lower = current_time
        if ALARM_LOWER:
            print("✅ Lower Zone: Roller running again. Alarm reset.")
            ALARM_LOWER = False
        cv2.putText(frame, "Lower Zone: RUNNING", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        if current_time - last_paint_lower > TIME_LIMIT and not ALARM_LOWER:
            cv2.putText(frame, "Lower Zone: STOPPED", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            winsound.Beep(2000, 1000)
            send_alert_mail("Lower Zone")
            ALARM_LOWER = True

    # Draw rectangles for zones
    cv2.rectangle(frame, (upper_zone[0], upper_zone[1]), (upper_zone[2], upper_zone[3]), (0,255,0), 2)
    cv2.rectangle(frame, (lower_zone[0], lower_zone[1]), (lower_zone[2], lower_zone[3]), (255,0,0), 2)

    cv2.imshow("Roller Monitoring System", frame)
    cv2.imshow("Upper Zone Mask", mask_upper)
    cv2.imshow("Lower Zone Mask", mask_lower)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()


