from PIL import Image, ImageDraw
import random, time, copy
from random import randint, randrange, choice
import sys, numpy, math

def initMatrix(matrix, xSize, ySize):
    for i in range(ySize):
        matrix.append(list())
        for j in range(xSize):
            matrix[i].append(0)
            
def weightMap(weight):
    # if weight > 0:
#         return 0
#     return 255
    return int(round(255 * (1/(math.exp(float(weight)/2))), 0))            

def getRandLine(xSize, ySize):
    return (random.uniform(-1, 1), randint(0,xSize), randint(0,ySize), randint(0,1))          

def randomizeLines(numLines, xSize, ySize):
    result = list();
    for i in range(numLines):
        result.append(getRandLine(xSize, ySize))
    return result
    
def getPixel(img, x, y):
    return img.getpixel((x,y))

def setPixel(img, x, y, value):
    img.putpixel((x, y), weightMap(value))
        
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
                    
def calcError(img, matrix, xSize, ySize):
    error = 0
    for y in range(ySize):
        for x in range(xSize):
            error += abs(weightMap(matrix[y][x]) - getPixel(img, x, y))
    return error

#adds a line and returns the change in total error that this action results in
def addLine(line, xSize, ySize):
    change = 0
    if(line[3] == 0): #(m, x0, y0, inverted)
        #not inverted
        for x in range(xSize): # y = m(x-x0) + y0
            yVal = int(round((x - line[1])*line[0] + line[2], 0))
            if(yVal >= 0 and yVal < ySize):
                change += weightMap(matrix[yVal][x] + 1) - weightMap(matrix[yVal][x])
                matrix[yVal][x] += 1
    else:
        #inverted
        for y in range(ySize): # x = m(y - y0) + x0
            xVal = int(round((y - line[2])*line[0] + line[1], 0))
            if(xVal >= 0 and xVal < xSize):
                change += weightMap(matrix[y][xVal] + 1) - weightMap(matrix[y][xVal])
                matrix[y][xVal] += 1
    return change

#adds a line and returns the change in total error that this action will results in
def removeLine(line, xSize, ySize):
    change = 0
    if(line[3] == 0): #(m, x0, y0, inverted)
        #not inverted
        for x in range(xSize): # y = m(x-x0) + y0
            yVal = int(round((x - line[1])*line[0] + line[2], 0))
            if(yVal >= 0 and yVal < ySize):
                newWeight = max(matrix[yVal][x] - 1, 0)
                change += weightMap(newWeight) - weightMap(matrix[yVal][x]);
                matrix[yVal][x] = newWeight
    else:
        #inverted
        for y in range(ySize): # x = m(y - y0) + x0
            xVal = int(round((y - line[2])*line[0] + line[1], 0))
            if(xVal >= 0 and xVal < xSize):
                newWeight = max(matrix[y][xVal] - 1, 0)
                change += weightMap(newWeight) - weightMap(matrix[y][xVal])
                matrix[y][xVal] = newWeight
    return change
    
def drawMatrix(matrix, xSize, ySize):
    image = Image.new('L', (128, 128), (255))
    for y in range(ySize):
        for x in range(xSize):
            setPixel(image, x, y, matrix[y][x])
    image.show()

def gTemp():
    matrix = list()
    img = Image.open("img/eye.jpg")
    xSize, ySize = img.size
    img.draft('L', img.size)
    
    initMatrix(matrix, xSize, ySize)
    lines = randomizeLines(500, xSize, ySize)
    fastDrawLines(lines, matrix, xSize, ySize)
    print(calcError(img, matrix, xSize, ySize))
    drawMatrix(matrix, xSize, ySize)
    

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

def main():
#Change image to desired test file
    im2 = Image.open("img/eye.jpg")
    width, height = im2.size
    im = Image.new('LA', (width, height), (255))

    draw = ImageDraw.Draw(im)

    #finalLines = randomLines(500, 1, width, height)

    finalLines = hillClimbing(250, 60, 1, height, width, im2)

    for line in finalLines:
        drawLine(line[0],line[1],width,height, line[2], draw)
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
        lines = randomLines(numbers, mRange, width, height)
        currentScore = scoreLines(lines, im2)
        if(bestSolution == None):
            bestSolution = copy.deepcopy(lines)
        tries = 0
        while(tries < 100 and time.time() - startTime < timeLimit):
            #pick a random line
            climbNum += 1
            print(climbNum)
            location = random.randrange(0, length)

            #swap out the line with a new one
            oldLine = lines[location]

            inverted = randint(0, 1)
            if inverted == 0:
                bRange = height
            else:
                bRange = width
            lines[location] = (random.uniform(-mRange, mRange),randint(-bRange,bRange), inverted)
            score = scoreLines(lines, im2)

            #check that move is an improvement
            if(score < currentScore):
                #if it is, reset tries, update currentScore, and update temperature
                tries = 0
                currentScore = score
            else:
                #if it isn't, swap it back and increment tries
                lines[location] = oldLine
                tries += 1
        #if the new solution is better that the old best solution, replace the old best
        if(currentScore < scoreLines(bestSolution, im2)):
            bestSolution = copy.deepcopy(lines)

    return bestSolution

def scoreLines(lines, im2):
    img1 = Image.new('LA', im2.size, (0, 0))
    draw = ImageDraw.Draw(img1)
    for aLine in lines:
        drawLine(aLine[0], aLine[1], im2.size[0], im2.size[1], aLine[2], draw)

    s = 0
    for band_index, band in enumerate(img1.getbands()):
        m1 = numpy.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
        m2 = numpy.array([p[band_index] for p in im2.getdata()]).reshape(*im2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s

#main()
gTemp()
