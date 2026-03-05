import math

class EventEngine:
    def __init__(self, scene_memory):
        self.memory = scene_memory
        self.active_interactions = set()

    def process(self):
        objects = self.memory.objects
        events = []

        ids = list(objects.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                obj1 = objects[ids[i]]
                obj2 = objects[ids[j]]

                if len(obj1["positions"]) == 0 or len(obj2["positions"]) == 0:
                    continue

                p1 = obj1["positions"][-1]
                p2 = obj2["positions"][-1]

                distance = math.dist(p1, p2)

                if distance < 100:  # interaction threshold
                    interaction_key = (ids[i], ids[j])

                    if interaction_key not in self.active_interactions:
                        event = f"{obj1['label']} interacts with {obj2['label']}"
                        events.append(event)
                        self.active_interactions.add(interaction_key)

        return events