#!/usr/bin/python3
import sys
from time import time

# Helper function for printing to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Setup and run experiment
def runSimulation(numSteps, radius, userLocations, intensityRatio):
    # Instantiate user list helper class
    eprint("     Setting up user registry... ", end="")
    startTime = time()
    from userregistry import UserRegistry
    ul = UserRegistry(userLocations, radius)
    eprint("complete ({:3.3f} sec)".format(time() - startTime))
    
    # Helper for obtaining gaussian distribution from intensity ratio
    from random import normalvariate
    def numXmits(iR, nU, minVal):
        return max(minVal, int(round(normalvariate(iR*nU, iR*nU/2))))
    
    # For each time step, send a random amount of messages
    for step in range(1,numSteps+1):
        numMsgs = numXmits(intensityRatio, len(userLocations), 0)
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

# Can be used elsewhere to build
def simArgParse():
    import argparse
    from argLimitedFloat import Range
    parser = argparse.ArgumentParser(description='Run a WMN simulation of N users')
    parser.add_argument('-R', '--radius', metavar='radius', type=float, default=10.0,
        choices=[Range(1,1000)], help='Broadcast radius [feet]')
    parser.add_argument('-T', '--steps', metavar='steps', type=int, default=10,
        choices=[Range(1,1000)], help='Number of steps in the simulation')
    parser.add_argument('-I', '--intensity-ratio', metavar='ratio', type=float, default=0.05,
        choices=[Range(0.001,0.1)], help='Average ratio of users that transmit every step')
    from userlist import addArgs
    addArgs(parser)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-U', '--users', metavar='users', type=int, choices=[Range(10,10000)], 
        help='The number of randomly generated users in the simulation')
    group.add_argument('-F', '--import-userlist', metavar='filename', type=str,
        help='A file containing a list of users in the simulation')
    
    args = parser.parse_args()

    if args.users:
        eprint("     Starting user generation... ", end="")
        startTime = time()
        from userlist import generateUserList
        userLocations = generateUserList(args)
        eprint("complete ({:3.3f} sec)".format(time() - startTime))
    elif args.import_userlist:
        eprint("     Starting userlist import... ", end="")
        startTime = time()
        from userlist import readUserList
        userLocations = readUserList(args.import_userlist)
        eprint("complete ({:3.3f} sec)".format(time() - startTime))
    
    simulationArguments = {}
    simulationArguments['numSteps']         = args.steps
    simulationArguments['radius']           = args.radius
    simulationArguments['userLocations']    = userLocations
    simulationArguments['intensityRatio']   = args.intensity_ratio
    
    return simulationArguments

if __name__ == '__main__':
    args = simArgParse()
    stats = runSimulation(**args)
    print("")
    print("Statistics:")
    print("\n".join(stats))
