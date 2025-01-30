class Job(object):
    def __init__(self, ind, length, kind, duration):
        self.number = ind
        self.length = length
        self.type = kind
        self.in_machine = -1
        self.duration = duration
        self.locked = False

    def __iter__(self):
        return iter(self)

    def __str__(self):
        return "[%s, %s, %s, %s]" % (self.number, self.length, self.type, self.duration)

    def __repr__(self):
        return "[%s, %s, %s, %s]" % (self.number, self.length, self.type, self.duration)

    def __len__(self):
        return self.length

    def __eq__(self, other):
        if self.number != other.number:
            return False
        else:
            return True

    def getNumber(self):
        return self.number

    def getLength(self):
        return self.length

    def getType(self):
        return self.type
    
    def getDuration(self):
        return self.duration
    
    def setDuration(self, duration):
        self.duration = duration
