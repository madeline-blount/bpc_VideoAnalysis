# Detector: object returned by YOLO to include object data, including tracking data

from ultralytics import YOLO

class Detector:
    def __init__(self, model_name="yolov8n.pt"):
        self.model = YOLO(model_name)

    def detect(self, frame_path):
        results = self.model.track(frame_path, persist=True)

        detections = []

        for result in results:
            boxes = result.boxes

            for box in boxes:
                if box.id is None:
                    continue

                class_id = int(box.cls[0])
                label = self.model.names[class_id]
                confidence = float(box.conf[0])
                track_id = int(box.id[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                detections.append({
                    "id": track_id,
                    "label": label,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2],
                    "center": (center_x, center_y)
                })

        return detections