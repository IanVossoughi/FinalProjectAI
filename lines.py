from PIL import Image, ImageDraw
import random, time, copy
from random import randint, randrange, choice
import sys, numpy

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
    args = sys.argv
    
    if (len(args) < 4):
        print("Usage: python " + args[0] + " [image path] [num lines] [time] [optional output filename]")
        return
    
#Change image to desired test file
    im2 = Image.open(args[1])
    width, height = im2.size
    im = Image.new('LA', (width, height), (255))

    draw = ImageDraw.Draw(im)

    #finalLines = randomLines(500, 1, width, height)

    finalLines = hillClimbing(int(args[2]), int(args[3]), 1, height, width, im2)

    for line in finalLines:
        drawLine(line[0],line[1],width,height, line[2], draw)
    print(scoreLines(finalLines, im))
    im.show()
    if (len(args) > 4):
        im.save("output/" + args[4])

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
    img1 = Image.new('LA', im2.size, (0,0))
    draw = ImageDraw.Draw(img1)
    for aLine in lines:
        drawLine(aLine[0], aLine[1], im2.size[0], im2.size[1], aLine[2], draw)

    s = 0
    for band_index, band in enumerate(img1.getbands()):
        m1 = numpy.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
        m2 = numpy.array([p[band_index] for p in im2.getdata()]).reshape(*im2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s

main()
