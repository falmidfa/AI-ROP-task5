# AI-ROP-task5
This project is a simple "Computer Vision" example that demonstrates how to detect and track colors in real-time using a webcam.
It uses **OpenCV**, **NumPy**, and **Pillow** to identify specific colors (yellow, blue, green, and purple) and draw bounding boxes around them.

---
 ## To run
  - Install the required libraries using the terminal (pip install opencv-python numpy pillow
)
  - Open the project in Visual Studio Code (VS Code) or any Python IDE

---

##  How it works
- Captures live video using OpenCV.
- Converts each frame to HSV for easier color segmentation.
- Defines color ranges for yellow, blue, green, and purple.
- Generates masks for each color and merges them.
- Highlights detected areas with rectangles labeled by color.
- Press ‘q’ to quit the program.

---

## Technologies Used
- **Python**
- **OpenCV** – image and video processing  
- **NumPy** – numerical operations  
- **Pillow (PIL)** – mask and bounding box detection

 
