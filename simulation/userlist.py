#!/usr/bin/python3
from random import random
from point import Point

def generateUserList(args):
    gridsize = Point(x=args.x, y=args.y)
    newLocation = lambda: Point(x=random()*gridsize.x, y=random()*gridsize.y)
    return [(uid, newLocation()) for uid in range(args.users)]

def readUserList(filename):
    
    with open(filename,'r') as f:
        lines = f.read().strip().split('\n')
    
    def readUser(line):
        fields = line.split(',')
        uid = int(fields[0])
        x = float(fields[1])
        y = float(fields[2])
        location = Point(x=x, y=y)
        return (uid, location)

    return [readUser(line) for line in lines]

def writeUserList(userList):

    def writeUser(user):
        uid = user[0]
        location = user[1]
        return "{},{},{}".format(uid, location.x, location.y)
    
    return "\n".join([ writeUser(u) for u in userList ])

from argLimitedFloat import Range
def addArgs(parser):
    parser.add_argument('-x', metavar='M', type=int, default=100,
        choices=[Range(10,1000)], help='The x-axis length M of the simulation grid')
    parser.add_argument('-y', metavar='N', type=int, default=100,
        choices=[Range(10,1000)], help='The y-axis length M of the simulation grid')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Create a randomized collection of some users '
        'on a MxN grid, and print to a file')
    addArgs(parser)
    parser.add_argument('users', metavar='users', type=int,
        choices=[Range(10,10000)], help='The number of users in the simulation')
    args = parser.parse_args()
    userList = generateUserList(args)

    print(writeUserList(userList))
