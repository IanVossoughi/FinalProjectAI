from PIL import Image, ImageDraw
import random, time, copy
from random import randint, randrange, choice
import sys, numpy

def initMatrix(matrix, xSize, ySize):
    for i in range(ySize):
        matrix.append(list())
        for j in range(xSize):
            matrix[i].append(0)

def weightMap(weight):
    if weight > 0:
        return 0
    return 255

def getRandLine(xSize, ySize):
    return (random.uniform(-1, 1), randint(0,xSize), randint(0,ySize), randint(0,1))

def randomizeLines(numLines, xSize, ySize):
    result = list();
    for i in range(numLines):
        result.append(getRandLine(xSize, ySize))
    return result

def getPixel(x, y, value, draw):
    pass

def setPixel(x, y, value, draw):
    draw.point((x, y), weightMap(value))

def fastDrawLines(lines, matrix, xSize, ySize):
    for line in lines:
        if(line[3] == 0): #(m, x0, y0, inverted)
            #not inverted
            for x in range(xSize): # y = m(x-x0) + y0
                yVal = int(round((x - line[1])*line[0] + line[2], 0))
                if(yVal >= 0 and yVal < ySize):
                    matrix[yVal][x] += 1
        else:
            #inverted
            for y in range(ySize): # x = m(y - y0) + x0
                xVal = int(round((y - line[2])*line[0] + line[1], 0))
                if(xVal >= 0 and xVal < xSize):
                    matrix[y][xVal] += 1

def fastDrawLine(slope, intercept, inverted, xSize, ySize):
    pass

def drawMatrix(matrix, xSize, ySize):
    image = Image.new('LA', (128, 128), (255))
    draw = ImageDraw.Draw(image)
    for y in range(ySize):
        for x in range(xSize):
            setPixel(x, y, matrix[y][x], draw)
    image.show()

def gTemp():
    matrix = list()
    initMatrix(matrix, 128, 128)
    lines = randomizeLines(100, 128, 128)
    fastDrawLines(lines, matrix, 128, 128)
    drawMatrix(matrix, 128, 128)

#funcitons above this point are functions for the fast implemenation im working on -Gianluca
def drawLine(slope, intercept, xSize, ySize, inverted, draw):
    if inverted == 0:
        x1 = 0
        x2 = xSize
        y1 = ySize - intercept
        y2 = ySize - (intercept + (slope * xSize))
    else:
        y1 = ySize
        y2 = 0
        x1 = xSize - intercept
        x2 = xSize - (intercept + (slope * ySize))
    draw.line((x1,y1, x2,y2), fill='Black')
    return draw

def drawSegs(point1, point2, draw):
    draw.line((point1[0],point1[1],point2[0],point2[1]),fill='Black')

def main():
#Change image to desired test file
    im2 = Image.open("img/hakkero.png")
    width, height = im2.size
    im = Image.new('LA', (width, height), (255))

    draw = ImageDraw.Draw(im)

    #finalLines = randomLines(500, 1, width, height)

    finalLines = hillClimbing(700, 300, 1, height, width, im2)

    for line in finalLines:
        drawSegs(line[0],line[1],draw)
        #drawLine(line[0],line[1],width,height, line[2], draw)
    print('\r')
    print(scoreLines(finalLines, im))
    im.show()

def randomLines(number, mRange, width, height):
    lineArray = []
    i = 0
    while i < number:
        inverted = randint(0, 1)
        if inverted == 0:
            bRange = height
        else:
            bRange = width
        lineArray.append((random.uniform(-mRange, mRange),randint(-bRange,bRange),inverted))
        i += 1
    return lineArray

def randomSegs(number, width, height):
    segArray = []
    i = 0
    while i < number:
        x1 = randint(0,width)
        x2 = randint(x1-10,x1+10)
        y1 = randint(0,height)
        y2 = randint(y1-10,y1+10)
        segArray.append(((x1,y1),(x2,y2)))
        i += 1
    return segArray

def hillClimbing(numbers, timeLimit, mRange, height, width, im2):
    #setup
    size = im2.size
    startTime = time.time()
    bestSolution = None
    length = numbers
    #keep searching for solution while there is time last
    while(time.time() - startTime < timeLimit):
        climbNum = 0
        #randomly create enough lines
        lines = randomSegs(numbers, width, height)
        #lines = randomLines(numbers, mRange, width, height)
        currentScore = scoreLines(lines, im2)
        if(bestSolution == None):
            bestSolution = copy.deepcopy(lines)
        tries = 0
        while(tries < 100 and time.time() - startTime < timeLimit):
            #pick a random line
            climbNum += 1
            sys.stdout.write('\r' + str(climbNum))
            sys.stdout.flush()
            location = random.randrange(0, length)

            #swap out the line with a new one
            oldLine = lines[location]

            inverted = randint(0, 1)
            if inverted == 0:
                bRange = height
            else:
                bRange = width

            #NewSeg
            x1 = randint(0, width)
            x2 = randint(x1 - 10, x1 + 10)
            y1 = randint(0, height)
            y2 = randint(y1 - 10, y1 + 10)
            lines[location] = ((x1,y1),(x2,y2))
            #EndNewSeg
            #lines[location] = ((randint(0,width),randint(0,height)),(randint(0,width),randint(0,height)))
            #lines[location] = (random.uniform(-mRange, mRange),randint(-bRange,bRange), inverted)
            score = scoreLines(lines, im2)

            #check that move is an improvement
            if(score > currentScore):
                #if it is, reset tries, update currentScore, and update temperature
                tries = 0
                currentScore = score
            else:
                #if it isn't, swap it back and increment tries
                lines[location] = oldLine
                tries += 1
        #if the new solution is better that the old best solution, replace the old best
        if(currentScore > scoreLines(bestSolution, im2)):
            bestSolution = copy.deepcopy(lines)
    return bestSolution

def scoreLines(lines, im2):
    img1 = Image.new('LA', im2.size, (0,0))
    draw = ImageDraw.Draw(img1)
    for aLine in lines:
        drawSegs(aLine[0],aLine[1],draw)
        #drawLine(aLine[0], aLine[1], im2.size[0], im2.size[1], aLine[2], draw)

    s = 0
    for band_index, band in enumerate(img1.getbands()):
        m1 = numpy.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
        m2 = numpy.array([p[band_index] for p in im2.getdata()]).reshape(*im2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s

main()
#gTemp()
