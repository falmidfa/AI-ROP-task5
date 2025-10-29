import cv2
import numpy as np
from PIL import Image

def get_limit(color_bgr):
    c = np.uint8([[color_bgr]]) 
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    hue = int(hsvC[0, 0, 0])
    lower = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8)
    upper = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8)
    return lower, upper


TARGETS = {
    "yellow": {"bgr": (0, 255, 255), "box": (0, 255, 255)},
    "blue":   {"bgr": (255, 0, 0),   "box": (255, 0, 0)},
    "green":  {"bgr": (0, 255, 0),   "box": (0, 255, 0)},
    "purple": {"bgr": (255, 0, 255), "box": (255, 0, 255)}, 
}

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise RuntimeError("❌ Could not open camera. Try index 0/1/2 and close other apps using the camera.")

# Precompute HSV limits
for name, cfg in TARGETS.items():
    cfg["lower"], cfg["upper"] = get_limit(cfg["bgr"])

kernel = np.ones((5,5), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Failed to grab frame.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    vis = frame.copy()

    for name, cfg in TARGETS.items():
        mask = cv2.inRange(hsv, cfg["lower"], cfg["upper"])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

        ys, xs = np.where(mask > 0)
        if xs.size and ys.size:
            x1, x2 = xs.min(), xs.max()
            y1, y2 = ys.min(), ys.max()
            cv2.rectangle(vis, (x1, y1), (x2, y2), cfg["box"], 3)
            cv2.putText(vis, name, (x1, max(y1 - 8, 0)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, cfg["box"], 2, cv2.LINE_AA)

        combined_mask = cv2.bitwise_or(combined_mask, mask)

    cv2.imshow("frame", vis)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
