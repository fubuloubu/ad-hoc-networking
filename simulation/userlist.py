#!/usr/bin/python3
from random import random
from point import Point

GRIDSIZE = Point(x=100.0, y=100.0) #feet

def generateUserList(numUsers):
    newLocation = lambda: Point(x=random()*GRIDSIZE.x, y=random()*GRIDSIZE.y)
    return [(uid, newLocation()) for uid in range(numUsers)]

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

def writeUser(user):
    uid = user[0]
    location = user[1]
    return "{},{},{}".format(uid, location.x, location.y)

if __name__ == '__main__':
    import argparse
    from argLimitedFloat import Range
    parser = argparse.ArgumentParser(description='Create a randomized collection of N users, and print to a file')
    parser.add_argument('users', metavar='N', type=int,
        choices=[Range(10,10000)], help='The number of users in the simulation')
    args = parser.parse_args()
    
    print( "\n".join([ writeUser(u) for u in generateUserList(args.users) ]))
