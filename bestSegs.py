from PIL import Image
import random, time, copy, math, sys, bisect
from random import randint, randrange, choice


def initMatrix(matrix, xSize, ySize):
    for i in range(ySize):
        matrix.append(list())
        for j in range(xSize):
            matrix[i].append(0)


def weightMap(weight):
    # if weight > 0:
    #         return 0
    #     return 255
    return int(round(255 / (math.exp(float(weight) / 2)), 0))


def getRandSeg(xSize, ySize):
    point1 = (random.randrange(0, xSize), random.randrange(0, ySize))
    point2 = (random.randrange(0, xSize), random.randrange(0, ySize))
    while (point2[0] == point1[0] and point2[1] == point1[1]):
        point2 = (random.randrange(0, xSize), random.randrange(0, ySize))
    return (point1, point2, -1)


def randomizeSegs(numSegs, xSize, ySize):
    result = list();
    for i in range(numSegs):
        result.append(getRandSeg(xSize, ySize))
    return result


def getPixel(img, x, y):
    return img.getpixel((x, y))


def setPixel(img, x, y, value):
    img.putpixel((x, y), weightMap(value))


def fastDrawSegs(segs, matrix, xSize, ySize, segLen, img):
    for i in range(len(segs)):  # ((x0,y0),(x1,y1))
        segs[i] = addSeg(segs[i], matrix, img, xSize, ySize, segLen)


def getError(img, matrix, x, y):
    return abs(weightMap(matrix[y][x]) - getPixel(img, x, y))


def calcError(img, matrix, xSize, ySize):
    error = 0
    for y in range(ySize):
        for x in range(xSize):
            error += getError(img, matrix, x, y)
    return error


# adds a line and returns the change in total error that this action results in
def addSeg(seg, matrix, image, xSize, ySize, segLen):
    change = 0
    if (abs(seg[0][0] - seg[1][0]) >= abs(seg[0][1] - seg[1][1])):
        start = min(seg[0][0], seg[1][0])
        end = max(seg[0][0], seg[1][0])
        end = min(end, start + segLen)
        for x in range(start, end + 1):  # y = ((y1-y0)/(x1-x0))(x - x0) + y0
            y = int(round((float((seg[1][1] - seg[0][1])) / (seg[1][0] - seg[0][0])) * (x - seg[0][0]) + seg[0][1], 0))
            if (y >= 0 and y < ySize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] += 1
                change += getError(image, matrix, x, y) - oldErr
    else:
        start = min(seg[0][1], seg[1][1])
        end = max(seg[0][1], seg[1][1])
        end = min(end, start + segLen)
        for y in range(start, end + 1):  # x = ((x1-x0)/(y1-y0))(y - y0) + x0
            x = int(round((float((seg[1][0] - seg[0][0])) / (seg[1][1] - seg[0][1])) * (y - seg[0][1]) + seg[0][0], 0))
            if (x >= 0 and x < xSize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] += 1
                change += getError(image, matrix, x, y) - oldErr
    return (seg[0], seg[1], change)


# adds a line and returns the change in total error that this action will results in
def removeSeg(seg, matrix, image, xSize, ySize, segLen):
    change = 0
    if (abs(seg[0][0] - seg[1][0]) >= abs(seg[0][1] - seg[1][1])):
        start = min(seg[0][0], seg[1][0])
        end = max(seg[0][0], seg[1][0])
        end = min(end, start + segLen)
        for x in range(start, end + 1):  # y = ((y1-y0)/(x1-x0))(x - x0) + y0
            y = int(round((float((seg[1][1] - seg[0][1])) / (seg[1][0] - seg[0][0])) * (x - seg[0][0]) + seg[0][1], 0))
            if (y >= 0 and y < ySize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] = max(matrix[y][x] - 1, 0)
                change += getError(image, matrix, x, y) - oldErr
    else:
        start = min(seg[0][1], seg[1][1])
        end = max(seg[0][1], seg[1][1])
        end = min(end, start + segLen)
        for y in range(start, end + 1):  # x = ((x1-x0)/(y1-y0))(y - y0) + x0
            x = int(round((float((seg[1][0] - seg[0][0])) / (seg[1][1] - seg[0][1])) * (y - seg[0][1]) + seg[0][0], 0))
            if (x >= 0 and x < xSize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] = max(matrix[y][x] - 1, 0)
                change += getError(image, matrix, x, y) - oldErr
    return change


def drawMatrix(matrix, xSize, ySize):
    image = Image.new('L', (xSize, ySize))
    for y in range(ySize):
        for x in range(xSize):
            setPixel(image, x, y, matrix[y][x])
    image.show()
    return image

def segKey(seg):
    return seg[2]

def addToLines(lines, seg):
    a = 0
    b = len(lines)
    while(a < b):
        pos = (a + b) / 2
        if(seg[2] > lines[pos][2]):
            a = pos + 1;
        else:
            b = pos
    lines.insert(a, seg)

def hillClimbing(path, numLines, timeLimit, segLen):
    # setup
    img = Image.open(path)
    xSize, ySize = img.size
    img.draft('L', img.size)

    matrix = list()
    startTime = time.time()
    bestSolution = None
    bestScore = None
    # keep searching for solution while there is time last
    while (time.time() - startTime < timeLimit):
        # randomly draw lines
        initMatrix(matrix, xSize, ySize)
        lines = randomizeSegs(numLines, xSize, ySize)
        fastDrawSegs(lines, matrix, xSize, ySize, segLen, img)
        lines.sort(key = segKey) #worst is at the end
        error = calcError(img, matrix, xSize, ySize)
        if (bestSolution == None):
            bestSolution = copy.deepcopy(matrix)
            bestScore = error
        tries = 0
        count = 0
        while (time.time() - startTime < timeLimit):
            # pick a random line and make it something else
            if(tries < 100):
                index = numLines-1
            else:
                index = random.randrange(0, numLines)
            oldLine = lines[index]
            newLine = getRandSeg(xSize, ySize)

            # change the line and get new score
            change = removeSeg(oldLine, matrix, img, xSize, ySize, segLen)
            newLine = addSeg(newLine, matrix, img, xSize, ySize, segLen)
            change += newLine[2]
            # check that the move is an improvement
            if (change < 0):
                # if it is, keep it
                lines.pop(index)
                addToLines(lines, newLine)
                error += change
                tries = 0
            else:
                # if not, switch the line back
                removeSeg(newLine, matrix, img, xSize, ySize, segLen)
                addSeg(oldLine, matrix, img, xSize, ySize, segLen)
                tries += 1
            count += 1
            sys.stdout.write("\r" + str(count) + ": " + str(error) + " -- " + "{0:.1f}".format(
                timeLimit - (time.time() - startTime)))
            sys.stdout.flush()
        # if the new solution is better that the old best solution, replace the old best
        if (error < bestScore):
            bestSolution = copy.deepcopy(matrix)
            bestScore = error

    print("")
    return (bestSolution, xSize, ySize)


def main():
    args = sys.argv
    if (len(args) < 5):
        print("Usage: python " + args[0] + " [image path] [num lines] [time] [segment length] [optional output filename")
        return
    result = hillClimbing(args[1], int(args[2]), int(args[3]), int(args[4]))
    image = drawMatrix(result[0], result[1], result[2])
    if (len(args) == 6):
        image.save("output/" + args[5])


main()
