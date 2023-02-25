import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    @property
    def empty(self) -> bool:
        return len(self.elements) == 0
    
    def add(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.elements)[1]
