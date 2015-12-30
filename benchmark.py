import datetime


class Benchmark:
    def __init__(self):
        self.timers = {}
        
    def start(self, name):
        self.timers[name] = datetime.datetime.now()
        
    def time(self, name):
        return float((datetime.datetime.now() - self.timers[name]) / 1e6) if name in self.timers else None