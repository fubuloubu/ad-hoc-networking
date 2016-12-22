#!/usr/bin/python3
from time import time
from eprint import eprint

# Setup and run experiment
def runSimulation(numSteps, intensityRatio, userList):
    # Instantiate user list helper class
    eprint("     Setting up user registry... ", end="")
    startTime = time()
    from userregistry import UserRegistry
    ul = UserRegistry(userList)
    eprint("complete ({:3.3f} sec)".format(time() - startTime))
    
    # Helper for obtaining gaussian distribution from intensity ratio
    from random import normalvariate
    def numXmits(iR, nU, minVal):
        return max(minVal, int(round(normalvariate(iR*nU, iR*nU/2))))
    
    # For each time step, send a random amount of messages
    for step in range(1,numSteps+1):
        numMsgs = numXmits(intensityRatio, len(userList), 0)
        eprint("Step {:02d} Sending {:02d} message(s)... ".format(step, numMsgs), end="")
        startTime = time()
        retransmissions = ul.sendMessages(step, numMsgs)
        eprint("complete ({:3.3f} sec)".format(time() - startTime))

    # Complete re-transmissions
    postSteps = 1
    while (postSteps <= 10 and retransmissions > 0):
        eprint("Step {:02d} Completing retransmit... ".format(postSteps+numSteps), end="")
        startTime = time()
        retransmissions = ul.sendMessages()
        eprint("complete ({:3.3f} sec)".format(time() - startTime))
        postSteps += 1
        
    # Compile statistics
    eprint("         Compiling Statistics... ", end="")
    startTime = time()
    stats = ul.userStatistics()
    eprint("complete ({:3.3f} sec)".format(time() - startTime))
    return stats

import argparse
# Can be used elsewhere to build
def simArgBuild(parser):
    parser.add_argument('-t', '--steps', metavar='steps', type=int, default=50,
        choices=[Range(1,1000)], help='Number of steps in the simulation')
    parser.add_argument('-i', '--intensity-ratio', metavar='ratio', type=float, default=0.05,
        choices=[Range(0.001,0.1)], help='Average ratio of users that transmit every step')
    
def simArgParse(args, userList):
    simulationArguments = {}
    simulationArguments['numSteps']         = args.steps
    simulationArguments['intensityRatio']   = args.intensity_ratio
    simulationArguments['userList']         = userList
    
    return simulationArguments

if __name__ == '__main__':
    from argLimitedFloat import Range
    parser = argparse.ArgumentParser(description='Run a WMN simulation of N users')
    simArgBuild(parser)
    from userlist import ulArgBuild, ulArgParse
    ulArgBuild(parser)
    
    args = parser.parse_args()
    userList = ulArgParse(args)
    simArgs = simArgParse(args, userList)
    
    stats = runSimulation(**simArgs)
    print("")
    print("Statistics:")
    print("\n".join(stats))
