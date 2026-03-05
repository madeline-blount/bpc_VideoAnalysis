# Enables persistent object identity & motion tracking

import time
import math

class SceneMemory:
    def __init__(self):
        self.objects = {}
        self.events = []

    def update(self, detections):
        current_time = time.time()

        for det in detections:
            obj_id = det["id"]

            if obj_id not in self.objects:
                self.objects[obj_id] = {
                    "label": det["label"],
                    "positions": [],
                    "last_seen": current_time,
                    "state": "new"
                }

            self.objects[obj_id]["positions"].append(det["center"])
            self.objects[obj_id]["last_seen"] = current_time

            # Keep only last 10 positions
            if len(self.objects[obj_id]["positions"]) > 10:
                self.objects[obj_id]["positions"].pop(0)

    def compute_velocity(self, obj_id):
        positions = self.objects[obj_id]["positions"]
        if len(positions) < 2:
            return 0

        x1, y1 = positions[-2]
        x2, y2 = positions[-1]

        return math.dist((x1, y1), (x2, y2))