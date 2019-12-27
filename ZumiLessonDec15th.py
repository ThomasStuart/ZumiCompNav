from zumi.zumi import Zumi
import time
import math

zumi = Zumi()
zumi.mpu.calibrate_MPU()

# CONSTANTS
DIV_CONST = 6.0
WHITE_GRID_SIZE = 0.8
BLACK_GRID_SIZE = 0.8
POWER = 40
TURN_DURATION = 0.60


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# dictionary with integer keys
dict = {'S': Point(0, 0),
        'A': Point(10, 5),
        'B': Point(15, 10),
        'C': Point(5, 10)
        }


def getTimeForTravel(dist):
    time = (dist + 1) / DIV_CONST
    return time


def gridDistToInches(gVal):
    if gVal == 0:
        return 0
    elif gVal == 1:
        return WHITE_GRID_SIZE
    else:
        # the negative 1 is due to their being 1 less black for every 2 whites
        return ((gVal * WHITE_GRID_SIZE) + ((gVal - 1) * BLACK_GRID_SIZE))

def getCoordinates(letter):
    pt = dict[letter]
    return pt


def dest2dest(startLetterDest, endLetterDest):
    # get coordinates for startDest
    pairStart = getCoordinates(startLetterDest)
    # get coordinates for endDest
    pairEnd = getCoordinates(endLetterDest)
    # carry out the point to point
    travelP2P(pairStart.x, pairStart.y, pairEnd.x, pairEnd.y)


# travelP2P moves zumi from one grid point
# to another.
# Logic:  points -> dist between points
#        -> time needed to travel length
def travelP2P(startX, startY, endX, endY):
    print("")

# Go from dest S (start) to dest A (first home)
print("-----S-A-----")
dest2dest('S', 'A')
time.sleep(5)
#zumi.turn_right(5)
print("-----S-A-----")
print()
print()
# Go from dest A to dest B
print("-----A-B-----")
dest2dest('A', 'B')
print("-----A-B-----")
print()
print()
time.sleep(5)
# Go from dest B to dest C
print("-----B-C-----")
dest2dest('B', 'C')
print("-----B-C-----")
#zumi.turn_right(5)
