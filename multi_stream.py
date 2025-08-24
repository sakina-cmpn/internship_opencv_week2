import cv2
import numpy as np
import threading
import time

# Configuration Section
# Example RTSP streams (replace with 4 working public RTSP URLs)
STREAM_URLS = [
    0,  # your laptop camera
    "./pexels-kelly-2909914-3840x2024-24fps.mp4",
    "./7578550-uhd_3840_2160_30fps.mp4",
    "./7578553-uhd_3840_2160_30fps.mp4"
]
#(Using 0 tells OpenCV to use your default webcam.)

FRAME_WIDTH = 320   # width of each video frame
FRAME_HEIGHT = 240  # height of each video frame

# Global variable to hold frames from each camera
frames = [np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8) for _ in STREAM_URLS]
locks = [threading.Lock() for _ in STREAM_URLS]

# Background subtractors for motion detection
bg_subtractors = [cv2.createBackgroundSubtractorMOG2() for _ in STREAM_URLS]

# Camera Thread Function

def capture_stream(stream_id, url):
    """Function to capture frames from a single camera in a thread"""
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open stream {stream_id}: {url}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"[WARNING] Stream {stream_id} disconnected")
            break

        # Resize frame to fixed size
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        # Store frame safely with lock
        with locks[stream_id]:
            frames[stream_id] = frame

    cap.release()

# Motion Detection Function
def detect_motion(stream_id, frame):
    """Detect motion using background subtraction"""
    fg_mask = bg_subtractors[stream_id].apply(frame)

    # Clean mask with morphological operations (remove noise)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))

    motion_pixels = cv2.countNonZero(fg_mask)

    if motion_pixels > 1500:  # lowered threshold
        return True
    return False

# Camera Integrity Check Function

def check_integrity(frame):
    """Check if camera is blurred, covered, or laser affected"""
    # If the frame is almost completely black → no signal
    if np.mean(frame) < 5:  
        return "No Signal"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 1. Blur detection using Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < 100:  # low variance means blur
        return "Blurred/Out of Focus"

    # 2. Coverage detection using histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist / hist.sum()
    max_val = hist.max()

    if max_val > 0.9:  # too uniform (covered or single color)
        return "Covered/Blocked"

    # 3. Laser / Overexposed detection (too bright or red dominated)
    mean_val = np.mean(frame)
    if mean_val > 240:  # very bright (white screen)
        return "Overexposed/Laser"

    return None  # no problem

# Main Function

def main():
    # Start one thread per camera
    threads = []
    for i, url in enumerate(STREAM_URLS):
        t = threading.Thread(target=capture_stream, args=(i, url))
        t.daemon = True
        t.start()
        threads.append(t)

    print("[INFO] All camera threads started")

    while True:
        display_frames = []

        for i in range(len(STREAM_URLS)):
            with locks[i]:
                frame = frames[i].copy()

            # Motion detection
            if detect_motion(i, frame):
                # Draw white rectangle for background
                cv2.rectangle(frame, (5, 5), (150, 35), (255, 255, 255), -1)
                cv2.putText(frame, "Motion Detected", (10, 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            # Camera integrity check
            status = check_integrity(frame)
            if status is not None:
                cv2.rectangle(frame, (5, 40), (200, 70), (0, 0, 255), -1)
                cv2.putText(frame, "NO SIGNAL", (10, 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            display_frames.append(frame)

        # Arrange frames in 2x2 grid
        top_row = np.hstack((display_frames[0], display_frames[1]))
        bottom_row = np.hstack((display_frames[2], display_frames[3]))
        grid = np.vstack((top_row, bottom_row))

        # Show window
        cv2.imshow("Multi-Stream Viewer", grid)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Run the program

if __name__ == "__main__":
    main()
