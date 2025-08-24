# OpenCV Week 2 – Real-Time Multi-Stream Viewer with Motion & Camera Integrity Detection

##  Project Overview

This project demonstrates a **real-time multi-stream video processing system** using **OpenCV** and **Python threading**. The system can:

* Capture and display 4 video streams (RTSP, local webcam, or video files) in a **2x2 grid**.
* Perform **real-time motion detection** using background subtraction.
* Perform **camera integrity checks** to detect if a feed is compromised (blurred, blocked, too dark, or too bright).

This project is part of **Week 2 OpenCV tasks**

##  Project Structure
```
opencv-week2/
├──  multi_stream.py 
├── week2_report.pdf      
├── diagrams/
│   ├── flow_diagram.png      
│   └── output.png        
└── README.md              
```
##  Requirements
* Python 3.8+
* OpenCV
* NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```
##  How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/opencv-week2.git
   cd opencv-week2
   ```

2. Navigate to the code directory:

   ```bash
   cd opencv-week2
   ```

3. Run the script:

   ```bash
   python multi_stream.py
   ```

4. Press **`q`** to quit the viewer.

---

## 🎯 Features

* **Multi-Stream RTSP Viewer**: Streams 4 video feeds simultaneously in a 2x2 grid.
* **Motion Detection**: Detects movement using background subtraction and overlays a message.
* **Camera Integrity Check**: Detects compromised feeds:

  * Blurred / Out of focus
  * Covered / Blocked
  * Overexposed (laser/bright light)
  * No signal (black screen)

---

## 📊 Workflow Diagram

See the diagram in `diagrams/flow_diagram.png`:

**Workflow:**

1. Capture video streams (threads)
2. Resize & preprocess frames
3. Apply motion detection & integrity checks
4. Combine into 2x2 grid
5. Display in real-time

## 📸 Example Output

* `diagrams/output.png` shows the 2x2 window with motion indicators.

##  Report

The detailed report is available in `report/week2_report.md` and includes:

* Objective
* Sources consulted
* Key learnings
* Challenges
* Results & screenshots
* Conclusion
