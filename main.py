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
TURN_DURATION = 0.67

# Globals
currentlyPointing = 'E'
currentX = 0
currentY = 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Stride:
    def __init__(self, direction, LoR, gridDist, NESW):
        self.direction = direction
        self.LoR = LoR
        self.gridDist = gridDist
        self.NESW = NESW


# dictionary with integer keys
dict = {'S': Point(0, 0),
        'A': Point(10, 5),
        'B': Point(15, 10),
        'C': Point(25, 0),
        'D': Point(5, 10),
        'E': Point(15, 20),
        'F': Point(20, 18)
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


def plotCourse(gridDistX, gridDistY):
    course = []
    moveDir = ''
    desiredDirectionX = ''
    desiredDirectionY = ''
    isInitalStride = True
    global currentX
    global currentY

    # WARNING: if not on corner, must move to one first
    # case 1:  X is non-corner but  Y is a corner
    # case 2:  X is corner     but not Y
    # case 3:  X && Y are non-corners  (DONT THINK THIS CAN HAPPEN)
    # case 4:  X && Y are both corner points
    checkNonCornerX = currentX % 10
    checkNonCornerY = currentY % 10

    if (checkNonCornerX != 0 and checkNonCornerY == 0):
        moveDir = 'x'
    elif (checkNonCornerX == 0 and checkNonCornerY != 0):
        moveDir = 'y'
    else:
        moveDir = 'x'

    if (gridDistX > 0):
        desiredDirectionX = 'E'
    else:
        desiredDirectionX = 'W'

    if (gridDistY > 0):
        desiredDirectionY = 'N'
    else:
        desiredDirectionY = 'S'

    currentX = currentX + gridDistX
    currentY = currentY + gridDistY

    gridDistX = abs(gridDistX)
    gridDistY = abs(gridDistY)

    moveToStartDirection(moveDir, desiredDirectionX, desiredDirectionY)
    turnX = getTurnX(desiredDirectionX, desiredDirectionY)
    turnY = getTurnY(turnX)

    while (gridDistX + gridDistY > 0):
        print('total: ', gridDistX + gridDistY)
        if (moveDir == 'x'):
            dx = 0
            if (gridDistX % 10 != 0):
                dx = gridDistX % 10
            else:
                dx = 10

            gridDistX = gridDistX - dx
            print('adding in x: ', dx)
            if (isInitalStride == True):
                course.append(Stride('x', 0, dx, desiredDirectionX))
                isInitalStride = False
            else:
                course.append(Stride('x', turnX, dx, desiredDirectionX))
        else:
            dy = 0
            if (gridDistY % 10 != 0):
                dy = gridDistY % 10
            else:
                dy = 10

            gridDistY = gridDistY - dy
            print('adding in y: ', dy)

            if (isInitalStride == True):
                course.append(Stride('y', 0, dy, desiredDirectionY))
                isInitalStride = False
            else:
                course.append(Stride('y', turnY, dy, desiredDirectionY))

            # Alternate to next dir
        if (moveDir == 'x'):
            course.append(Stride('n', turnX, 0, 0))
            moveDir = 'y'
        else:
            course.append(Stride('n', turnY, 0, 0))
            moveDir = 'x'

    course.pop(len(course) - 1)
    return course


def moveToStartDirection(moveDir, desiredDirectionX, desiredDirectionY):
    global currentlyPointing
    # if front of the car is facing wrong direction of intial moveDir
    if (moveDir == 'x'):
        if (desiredDirectionX == 'E' and currentlyPointing == 'N'):
            zumi.turn_left(90)
        elif (desiredDirectionX == 'W' and currentlyPointing == 'N'):
            zumi.turn_right(90)
        elif (desiredDirectionX == 'E' and currentlyPointing == 'S'):
            zumi.turn_right(90)
        elif (desiredDirectionX == 'W' and currentlyPointing == 'S'):
            zumi.turn_left(90)
        elif (desiredDirectionX == 'E' and currentlyPointing == 'W'):
            zumi.turn_left(180)
        elif (desiredDirectionX == 'W' and currentlyPointing == 'E'):
            zumi.turn_left(180)
    else:
        if (desiredDirectionY == 'N' and currentlyPointing == 'E'):
            zumi.turn_right(90)
        elif (desiredDirectionY == 'S' and currentlyPointing == 'E'):
            zumi.turn_left(90)
        elif (desiredDirectionY == 'N' and currentlyPointing == 'W'):
            zumi.turn_left(90)
        elif (desiredDirectionY == 'S' and currentlyPointing == 'W'):
            zumi.turn_right(90)
        elif (desiredDirectionY == 'N' and currentlyPointing == 'S'):
            zumi.turn_left(180)
        elif (desiredDirectionY == 'S' and currentlyPointing == 'N'):
            zumi.turn_left(180)


def getTurnX(ang1, ang2):
    if (ang1 == 'E' and ang2 == 'N'):
        return 'L'
    elif (ang1 == 'E' and ang2 == 'S'):
        return 'R'
    elif (ang1 == 'W' and ang2 == 'N'):
        return 'R'
    else:
        return 'L'


def getTurnY(dir):
    if (dir == 'L'):
        return 'R'
    else:
        return 'L'


# travelP2P moves zumi from one grid point
# to another.
# Logic:  points -> dist between points
#        -> time needed to travel length
def travelP2P(startX, startY, endX, endY):
    global currentlyPointing
    # dx = endX - startX  (grid)
    # dy = endY - startY  (grid)
    dxGrid = endX - startX
    dyGrid = endY - startY

    strides = plotCourse(dxGrid, dyGrid)
    print('length: ', len(strides))

    while (len(strides) != 0):
        # distance is in INCHES not GRID (CONVERT)

        print('strid@ dir, ', strides[0].direction)
        print('strid@ gridDist, ', strides[0].gridDist)
        print('strid@ NESW, ', strides[0].NESW)

        if (strides[0].direction != 'n'):
            moveNumInches = gridDistToInches(strides[0].gridDist)
            dtToMoveInches = getTimeForTravel(moveNumInches)

            if dtToMoveInches != 0:
                zumi.forward(POWER, dtToMoveInches)

            currentlyPointing = strides[0].NESW  # Useful for next movement
        else:
            # TODO: debug corner movement
            time.sleep(2)  # Wait 2 seconds
            zumi.forward(40, TURN_DURATION)

            if (strides[0].LoR == 'L'):
                zumi.turn_left(90)
            else:
                zumi.turn_right(90)

        del strides[0]

    # TODO: perform pickup or drop off


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

# Go from dest S (start) to dest A (first home)
print("-----S-A-----")
dest2dest('S', 'A')
print("-----S-A-----")
print()
print()
# Go from dest A to dest B
print("-----A-B-----")
dest2dest('A', 'B')
print("-----A-B-----")
print()
print()
print("-----B-D-----")
# Go from dest B to dest D
dest2dest('B', 'D')
print("-----B-D-----")
print()
print()
print("-----D-C-----")
dest2dest('D', 'C')
print("-----D-C-----")
# letter destinations -> grid points
# grid points -> distance between points
# process a course by angles and distances
# carry out the