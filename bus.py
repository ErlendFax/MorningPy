class Buss:
    def __init__(self, node):
        self.node = node
        self.expectedTime = None

    def addAimedTime(self,aimedTime):
        self.aimedTime = aimedTime

    def addExpectedTime(self, expectedTime):
        # consider adding here
        self.expectedTime = expectedTime

    def getExpectedUntilDeparture(self):
        if self.expectedTime == None:
            return None

        now = datetime.datetime.now()
        expected = datetime.datetime.combine(now, self.expectedTime)
        return expected - now

    # remove functions below when unified into getTime()
    def returnAimedTime(self):
        return self.aimedTime

    def returnExpectedTime(self):
        return self.expectedTime

