class Buss:
    def __init__(self, node):
        self.node = node
        self.realtime = None

    def addTime(self, time, realtime=False):
        if realtime == False:
            self.aimedtime = time
        else:
            self.realtime = time

    def getDepartureTime(self):
        if self.realtime == None:
            return self.aimedtime
        else:
            return self.realtime


