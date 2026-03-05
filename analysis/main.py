import os
import time
from detector import Detector
from scene_memory import SceneMemory
from event_engine import EventEngine

"""
Fondation of real time gameplay analysis system.
This system can track identity, compute motion, detect interactions. 
Events are only emitted when triggered. 
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAME_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "extracted_frames"))

detector = Detector()
memory = SceneMemory()
event_engine = EventEngine(memory)

while True:
    for root, dirs, files in os.walk(FRAME_FOLDER):
        for file in files:
            if file.endswith(".jpg"):
                frame_path = os.path.join(root, file)

                detections = detector.detect(frame_path)
                memory.update(detections)

                events = event_engine.process()

                for event in events:
                    print("[EVENT]", event)

    time.sleep(0.1)