from PIL import Image, ImageDraw
import random, time, copy
from random import randint, randrange, choice
import sys, numpy

def initMatrix(matrix, xSize, ySize):
    for i in range(ySize):
        matrix.append(list())
        for j in range(xSize):
            matrix[i].append(0)
            
def getRandLine(xSize, ySize):
    return (random.uniform(-mRange, mRange), randint(-bRange,bRange), randint(0,1))          

def randomizeLines(matrix, numLines, xSize, ySize):
    result = list();
    for(i in range(numLines)):
        result[i] = getRandLine()
        
def fastDrawLines(lines, matrix, xSize, ySize):
    for line in lines:
        if(line[2] == 0) {
            #not inverted
            for x in range(xSize):
                pass
        } else {
            #inverted
            for y in range(ySzie):
                pass
        }

def fastDrawLine(slope, intercept, inverted, xSize, ySize):
    pass

#funcitons above this point are functions for the fast implemenation im working on -Gianluca

def drawLine(slope, intercept, xSize, ySize, draw):
    x1 = 0
    x2 = xSize
    y1 = ySize - intercept
    y2 = ySize - (intercept + (slope * xSize))
    draw.line((x1,y1, x2,y2), fill='Black')
    return draw

def main():
#Change image to desired test file
    im2 = Image.open("img/eye.jpg")
    width, height = im2.size
    im = Image.new('LA', (width, height), (255))

    draw = ImageDraw.Draw(im)

    finalLines = hillClimbing(150, 1, 1, height, im2)

    for line in finalLines:
        drawLine(line[0],line[1],width,height,draw)
    print(scoreLines(finalLines, im))
    im.show()

def randomLines(number, mRange, bRange):
    lineArray = []
    i = 0
    while i < number:
        lineArray.append((random.uniform(-mRange, mRange),randint(-bRange,bRange)))
        i += 1
    return lineArray

def hillClimbing(numbers, timeLimit, mRange, bRange, im2):
    #setup
    size = im2.size
    startTime = time.time()
    bestSolution = None
    length = numbers
    #keep searching for solution while there is time last
    while(time.time() - startTime < timeLimit):
        climbNum = 0
        #randomly create enough lines
        lines = randomLines(numbers, mRange, bRange)
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
            lines[location] = (random.uniform(-mRange, mRange),randint(-bRange,bRange))
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
        drawLine(aLine[0], aLine[1], im2.size[1], im2.size[0], draw)

    s = 0
    for band_index, band in enumerate(img1.getbands()):
        m1 = numpy.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
        m2 = numpy.array([p[band_index] for p in im2.getdata()]).reshape(*im2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s

main()