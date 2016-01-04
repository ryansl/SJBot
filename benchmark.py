import time


class Benchmark:
    def __init__(self):
        self.timers = {}
        
    def start(self, name):
        self.timers[name] = time.time()
        return self.timers[name]

    def clear(self, name):
        del self.timers[name]
        
    def time(self, name):
        return round(float(time.time() - self.timers[name]), 3) if name in self.timers else float(0.000)