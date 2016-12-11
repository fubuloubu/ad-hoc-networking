#!/usr/bin/python3
from random import random
from point import Point
from time import time
from eprint import eprint

def generateUserList(args):
    gridsize = Point(x=args.x, y=args.y)
    newLocation = lambda: Point(x=random()*gridsize.x, y=random()*gridsize.y)
    return [(uid, newLocation(), args.radius) for uid in range(args.users)]

def readUserList(filename):
    
    with open(filename,'r') as f:
        lines = f.read().strip().split('\n')
    
    def readUser(line):
        fields = line.split(',')
        uid = int(fields[0])
        x = float(fields[1])
        y = float(fields[2])
        radius = float(fields[3])
        location = Point(x=x, y=y)
        return (uid, location, radius)

    return [readUser(line) for line in lines]

def writeUserList(userList):

    def writeUser(user):
        uid = user[0]
        location = user[1]
        radius = user[2]
        return "{},{},{},{}".format(uid, location.x, location.y, radius)
    
    return "\n".join([ writeUser(u) for u in userList ])

def genUserGraph(userList):
    import numpy as np
    # Get locations
    x = np.asarray(list(map(lambda u: u[1].x,           userList)))
    y = np.asarray(list(map(lambda u: u[1].y,           userList)))
    a = np.asarray(list(map(lambda u: np.pi * (u[2])**2,  userList)))
    colors = np.random.rand(len(x))
    # Draw reception radius as lightly colored circles
    plt.scatter(x, y, s=a, c=colors, alpha=0.5)
    # Draw small black dots in the middle to reprsent user location
    plt.scatter(x, y, s=np.pi, c='k')

import argparse
from argLimitedFloat import Range
def ulArgBuild(parser):
    parser.add_argument('-x', metavar='M', type=int, default=100,
        choices=[Range(10,1000)], help='The x-axis length M of the simulation grid')
    parser.add_argument('-y', metavar='N', type=int, default=100,
        choices=[Range(10,1000)], help='The y-axis length M of the simulation grid')
    parser.add_argument('-R', '--radius', metavar='radius', type=float, default=10.0,
        choices=[Range(1,1000)], help='Broadcast radius [feet]')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-U', '--users', metavar='users', type=int, choices=[Range(10,10000)], 
        help='The number of randomly generated users in the simulation')
    group.add_argument('-F', '--import-userlist', metavar='filename', type=str,
        help='A file containing a list of users in the simulation')

def ulArgParse(args):
    if args.users:
        eprint("     Starting user generation... ", end="")
        startTime = time()
        userLocations = generateUserList(args)
        eprint("complete ({:3.3f} sec)".format(time() - startTime))
    elif args.import_userlist:
        eprint("     Starting userlist import... ", end="")
        startTime = time()
        userLocations = readUserList(args.import_userlist)
        eprint("complete ({:3.3f} sec)".format(time() - startTime))

    return userLocations

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a randomized collection of some users '
        'on a MxN grid, and print to a file')
    ulArgBuild(parser)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--print-userlist', action='store_const', dest="action", const="print-ul",
            help='Print out to stdout the userlist')
    group.add_argument('--show-usergraph', action='store_const', dest="action", const="show-ug",
            help='Display a graph of user locations in a popup window')
    group.add_argument('--print-usergraph', action='store_const', dest="action", const="print-ug",
            help='Print out to stdout a TikZ-compatible graph of user locations')
    parser.set_defaults(action="print-ul")
    
    args = parser.parse_args()
    userList = ulArgParse(args)

    if args.action == "print-ul":
        print(writeUserList(userList))
    else: 
        import matplotlib.pyplot as plt
        genUserGraph(userList)
        if args.action == "show-ug":
            plt.show()
        elif args.action == "print-ug":
            from matplotlib2tikz import save as tikz_save
            tikz_save('output-graph.tex')
