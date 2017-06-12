import time

class Timer(object):
    def __init__(self):
        self.startTime = float('-inf')
    
    def start(self):
        self.startTime = time.clock()
    
    def stop(self):
        self.startTime = float('-inf')
    
    def get_time(self):
        return time.clock() - self.startTime
