import cv2
import time
import requests

SERVER_URL = "http://localhost:8000/upload"  # Replace with your backend endpoint

def capture_and_send():
    cap = cv2.VideoCapture(0)  # Open webcam (0 is default)

    if not cap.isOpened():
        print("Error: Cannot access camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Save the image temporarily
            filename = "frame.jpg"
            cv2.imwrite(filename, frame)

            # Send to backend
            with open(filename, "rb") as f:
                files = {"file": f}
                response = requests.post(SERVER_URL, files=files)
                print("Sent:", response.status_code)

            time.sleep(10)  # capture every 10 seconds
    finally:
        cap.release()

if __name__ == "__main__":
    capture_and_send()
