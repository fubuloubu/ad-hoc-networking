from point import dist
from message import Message

MAXSTACKLEN = 10

class CellPhoneUser:
    def __init__(self, userID, radius, location, registry):
        self.userID = userID
        self.radius = radius
        self.location = location
        self.registry = registry
    
    # Used for printing
    def __repr__(self):
        return "{0} class [ id: {1}, location: ({2}, {3}), radius: {4}, xmitMsgs: {5}" +\
                "recvMsgs: {6} ]".format(self.__class__.__name__, self.userID, 
                        self.location.x, self.location.y, self.radius,
                        self.xmitMsgs, self.recvMsgs)
    
    # Instance Variables
    # (During simulation)
    rcvdMsgs = []
    xmitMsgs = []
    reXmitStack = []
    
    # Receive message from remote user and store
    # if user is destination, else re-transmit
    # if criteria is met based on protocol
    def receive(self, msg):
        if self.userID == msg.rcvrID:
            msg.setReceiveTime()
            self.rcvdMsgs.append(msg)
        elif self.userID not in msg.XmitList and msg.TTL > 0:
            # message has not reached it's dest
            self.reXmitStack.append(msg)
            if len(self.reXmitStack) > MAXSTACKLEN:
                self.reXmitStack.pop(0)
        #else: message was retransmitted back to us
        #   ignore
    
    # Process and transmit provided message
    def transmit(self, msg):
        self.xmitMsgs.append(msg)
        self.broadcast(msg)
    
    # Re-transmit any messages that did not make it
    def reTransmit(self):
        if len(self.reXmitStack) > 0:
            msg = self.reXmitStack.pop()
            msg.incrTransTime()
            msg.addXmtr(self.userID)
            self.broadcast(msg)
            return 1 #message was sent
        return 0 #message was not sent
        
    # Return true if 2 unique users
    # are in range of each other
    def inRange(self, xmtr):
        return False if self == xmtr else \
            dist(self.location, xmtr.location) < self.radius

    # Broadcast message, whoever can hear it will try and process it
    def broadcast(self, msg):
        rcvrList = filter(lambda u: u.inRange(self), self.registry.userList)
        [u.receive(msg) for u in rcvrList]
