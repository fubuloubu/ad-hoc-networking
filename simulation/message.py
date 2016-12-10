from random import choice

class Message:
    def __init__(self, xmtrID, step, numUsers, TTL):
        self.xmtrID = xmtrID
        self.sentTime = step
        self.msg = "Sent at step {}".format(step)
        self.recvTime = None
        self.transitTime = 0
        
        self.XmitList = []
        self.addXmtr(self.xmtrID)
        self.TTL = TTL

        # Make a random choice of receiver
        # Note: cannot be same as transmitter
        validRcvrs = list(range(numUsers))
        validRcvrs.remove(self.xmtrID)
        
        self.rcvrID = choice(validRcvrs)
    
    # Add current transmitter to transmit list
    def addXmtr(self, xmtrID):
        self.XmitList.append(xmtrID)
    
    # Increment transit time
    def incrTransTime(self):
        self.transitTime += 1
        self.TTL -= 1
    
    # Record Message receipt
    def setReceiveTime(self):
        self.recvTime = self.transitTime + self.sentTime
    
    # Used for printing
    def __repr__(self):
        return "{} class [ ".format(self.__class__.__name__) + \
                    "{} @{} -> ".format(self.xmtrID, self.sentTime) + \
                    "{} @{}, ".format(self.rcvrID, self.recvTime) + \
                    "transit time: {}, ".format(self.transitTime) + \
                    "msg: {} ".format(self.msg) + \
                "]"
