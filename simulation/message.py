from random import choice

class Message:
    def __init__(self, xmtrID, step, numUsers):
        self.xmtr = xmtrID
        self.sentTime = step
        self.msg = "Sent at step {}".format(step)
        self.recvTime = None
        self.transitTime = 0

        # Make a random choice of receiver
        # Note: cannot be same as transmitter
        validRcvrs = list(range(numUsers))
        validRcvrs.remove(xmtrID)
        
        self.rcvr = choice(validRcvrs)
    
    # Increment transit time
    def incrTransTime(self):
        self.transitTime += 1
    
    # Record Message receipt
    def setReceiveTime(self):
        self.recvTime = self.transitTime + self.sentTime
    
    # Used for printing
    def __repr__(self):
        return "{} class [ ".format(self.__class__.__name__) + \
                    "{} @{} -> ".format(self.xmtr, self.sentTime) + \
                    "{} @{}, ".format(self.rcvr, self.recvTime) + \
                    "transit time: {}, ".format(self.transitTime) + \
                    "msg: {} ".format(self.msg) + \
                "]"
