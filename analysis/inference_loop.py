import cv2 # Reads images
import os # File navigation
import time # Loop timing
from PIL import Image 

print("Starting script")

from ultralytics import YOLO # Comp vision model
print("Imported YOLO")


model = YOLO("yolov8n.pt") # downloads pretrained model using COCO dataset (80 classes))
print("Model loaded")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAME_FOLDER = os.path.join(BASE_DIR, "..", "extracted_frames")
FRAME_FOLDER = os.path.abspath(FRAME_FOLDER)

print("Frames:", os.listdir(FRAME_FOLDER))

processed_files = set()

while True:
    subfolders = os.listdir(FRAME_FOLDER)

    for folder in subfolders:
        folder_path = os.path.join(FRAME_FOLDER, folder)

        # Skip if not a directory
        if not os.path.isdir(folder_path):
            continue

        files = os.listdir(folder_path)

        for file in files:
            if file.endswith(".jpg"):
                unique_id = f"{folder}/{file}"

                if unique_id not in processed_files:
                    image_path = os.path.join(folder_path, file)
                    print(f"\nProcessing {unique_id}")

                    results = model.track(image_path, persist=True) # Track objects across frames

                    for result in results:
                        boxes = result.boxes

                        frame_detections = []

                        for box in boxes:
                            class_id = int(box.cls[0])
                            confidence = float(box.conf[0])
                            label = model.names[class_id]
                            coords = box.xyxy[0].tolist()

                            detection = {
                                "label": label,
                                "confidence": confidence,
                                "bbox": coords
                            }

                            frame_detections.append(detection)

                            print(f"Detected: {label} ({confidence:.2f})")

                    processed_files.add(unique_id)

    time.sleep(0.5)