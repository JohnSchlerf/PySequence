import os
if os.name == 'nt':
    from time import clock as CurrentTime
    import time
    ADJUST_FOR_EPOCH = time.time()
else:
    from time import time as CurrentTime
    ADJUST_FOR_EPOCH = 0

class Clock:

    def __init__(self,numTimers):
        self.timers = []
        for i in range(numTimers):
            self.timers.append(0.0)
        self.resetAll()

    def __getitem__(self,key):
        return self.timers[key]

    def __setitem__(self,key,value):
        self.timers[key] = value

    def update(self):
        self.dt = CurrentTime()+ADJUST_FOR_EPOCH - self.lastTime
        self.lastTime += self.dt
        for i in range(len(self.timers)):
            self.timers[i] += self.dt
        
    def reset(self,whichTimer):
        self.timers[whichTimer] = 0.0

    def resetAll(self):
        self.initialTime = CurrentTime()+ADJUST_FOR_EPOCH
        self.lastTime = self.initialTime
        self.dt = 0
        for i in range(len(self.timers)):
            self.timers[i] = 0.0
