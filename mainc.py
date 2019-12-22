import time
import math


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
    global currentX
    global currentY

    checkNonCornerX = currentX % 10
    checkNonCornerY = currentY % 10

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


    turnX = getTurnX(desiredDirectionX, desiredDirectionY, gridDistX, gridDistY)
    turnY = getTurnY(turnX ,gridDistX , gridDistY )

    if (checkNonCornerX != 0 and checkNonCornerY == 0):
        moveDir = 'y'
        course.append(Stride('x', 0, checkNonCornerX, desiredDirectionX))
        course.append(Stride('n', turnX, 0, 0))
        gridDistX = gridDistX - checkNonCornerX
    elif (checkNonCornerX == 0 and checkNonCornerY != 0):
        moveDir = 'x'
        course.append(Stride('y', 0, checkNonCornerY, desiredDirectionY))
        course.append(Stride('n', turnY, 0, 0))
        gridDistY = gridDistY - checkNonCornerY
    else:
        moveDir = 'x'

    # moveToStartDirection(moveDir, desiredDirectionX, desiredDirectionY)

    while (gridDistX + gridDistY > 0):
        turnToken = False

        if (moveDir == 'x'):
            if( gridDistX > 0):
                turnToken = True
                dx = 0
                if (gridDistX >= 10):
                    dx = 10
                else:
                    dx = gridDistX

                gridDistX = gridDistX - dx
                course.append(Stride('x', turnX, dx, desiredDirectionX))
        else:
            if(gridDistY > 0 ):
                turnToken = True
                dy = 0
                if (gridDistY > 10):
                    dy = 10
                else:
                    dy = gridDistY

                gridDistY = gridDistY - dy
                course.append(Stride('y', turnY, dy, desiredDirectionY))


        # Alternate to next dir
        if (moveDir == 'x'):
            if turnToken and gridDistY != 0:
                course.append(Stride('n', turnX, 0, 0))
            elif turnToken and gridDistY == 0:
                course.append(Stride('n', 'S', 0, 0))

            moveDir = 'y'
        else:
            if turnToken and gridDistX != 0 :
                course.append(Stride('n', turnY, 0, 0))
            elif turnToken and gridDistY == 0:
                course.append(Stride('n', 'S', 0, 0))
            moveDir = 'x'


    course.pop(len(course) - 1)
    return course


def getTurnX(ang1, ang2, gx,gy):
    if gx == 0 or gy == 0:
        return 'S'

    if (ang1 == 'E' and ang2 == 'N'):
        return 'L'
    elif (ang1 == 'E' and ang2 == 'S'):
        return 'R'
    elif (ang1 == 'W' and ang2 == 'N'):
        return 'R'
    else:
        return 'L'


def getTurnY(dir, gx, gy):
    if gx == 0 or gy == 0:
        return 'S'

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
    counter = 0
    while (len(strides) != 0):
        # distance is in INCHES not GRID (CONVERT)
        print( "Stride: ", counter)
        counter = counter + 1
        print('\t dir       : ', strides[0].direction)
        print('\t dist moved: ', strides[0].gridDist)
        print('\t NESW      : ', strides[0].NESW)

        if (strides[0].direction != 'n'):
            moveNumInches = gridDistToInches(strides[0].gridDist)
            dtToMoveInches = getTimeForTravel(moveNumInches)

            if dtToMoveInches != 0:
                print("")
                # zumi.forward(POWER, dtToMoveInches)

            currentlyPointing = strides[0].NESW  # Useful for next movement
        else:
            # TODO: debug corner movement
            time.sleep(2)  # Wait 2 seconds
            # zumi.forward(40, TURN_DURATION)

            if (strides[0].LoR == 'L'):
                print("Turned Left")
                # zumi.turn_left(90)
            elif (strides[0].LoR == 'R'):
                print("Turned Right")
                # zumi.turn_right(90)
            else:
                print("Straight")

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


print()
print()
print("-----C-B-----")
dest2dest('C', 'B')
print("-----C-B-----")

# letter destinations -> grid points
# grid points -> distance between points
# process a course by angles and distances
# carry out the