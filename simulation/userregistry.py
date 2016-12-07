from random import shuffle
from itertools import permutations
from user import CellPhoneUser
from message import Message

class UserRegistry:
    def __init__(self, userLocations, radius):
        self.numUsers = len(userLocations)
        self.userList = [CellPhoneUser(uid, radius, location, self) \
                            for (uid, location) in userLocations]
        # For statistics later
        self.msgList = []
        self.retransmissions = 0

    # Used for printing
    def __repr__(self):
        return "{} class:".format(self.__class__.__name__) + \
            "\n".join([u.__repr__() for u in self.userList])
    
    # Send N messages from one 
    # random user to another
    def sendMessages(self, step=0, numMsgs=0):
        
        # Grab a random subset of N users
        shuffle(self.userList)
        xmtrList = self.userList[:numMsgs]
        
        # Send out calls
        for x in xmtrList:
            msg = Message(x.userID, step, self.numUsers)
            self.msgList.append(msg)
            x.transmit(msg)
        
        # Run re-transmission routine
        retransmissions = sum([u.reTransmit() for u in self.userList])
        self.retransmissions += retransmissions
        return retransmissions
    
    def userStatistics(self):
        totalMsgs =  len(self.msgList)
        successfulMsgs = filter(lambda m: m.recvTime is not None, self.msgList)
        numSuccessfulMsgs = len(list(successfulMsgs))
        
        successRate = 100*numSuccessfulMsgs/float(totalMsgs) if totalMsgs > 0 else 0
        avgLatency = sum(map(lambda m: m.transitTime, successfulMsgs))
        avgLatency = avgLatency/float(numSuccessfulMsgs) if numSuccessfulMsgs > 0 else 0
        
        # Return array of statistics
        return ["Total Messages: {}".format(totalMsgs),
                "Succesfully Received Messages: {}".format(numSuccessfulMsgs),
                "Success Rate: {:2.2f}%".format(successRate),
                "Number of Retransmissions: {}".format(self.retransmissions),
                "Average Latency: {:2.2f} [steps]".format(avgLatency)]
