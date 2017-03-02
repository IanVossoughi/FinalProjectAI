from PIL import Image, ImageDraw
import random, time, copy
from random import randint, randrange, choice
import sys, numpy

def main():
#Change image to desired test file
    refImage = Image.open("img/eye.jpg")
    #width, height = referenceImage.size
    #canvas = Image.new('LA', (width, height), (255))

    #canvasDrawing = ImageDraw.Draw(canvas)

    finalRects = hillClimb(200, refImage, 120)
    #rects = generateRectangles(canvas, 30)
    #drawRectangles(canvas, rects)

    #print(scoreRectangles(rects, referenceImage))

    #finalLines = hillClimbing(500, 60, 1, height, canvas)

    '''for line in finalLines:
        drawLine(line[0],line[1],width,height,draw)
    print(scoreLines(finalLines, im))'''
    #canvas.show()

def hillClimb(numRects, refImage, timeLimit):
    startTime = time.time()
    bestSolution = generateRectangles(refImage, numRects)
    score = scoreRectangles(bestSolution, refImage)


    while(time.time() - startTime < timeLimit):
        climbNum = 0
        tries = 0
        currSolution = generateRectangles(refImage, numRects)
        currScore = scoreRectangles(currSolution, refImage)
        if currScore > score:
            score = currScore
            bestSolution = copy.deepcopy(currSolution)
        bestCurrScore = score
        while(tries < 100 and time.time() - startTime < timeLimit):
            climbNum += 1
            rectNum = random.randint(0, numRects-1)
            
            oldRect = currSolution[rectNum]
            currSolution[rectNum] = generateRectangle(refImage)
            currScore = scoreRectangles(currSolution, refImage)
            if currScore > bestCurrScore:
                tries = 0
                bestCurrScore = currScore
            else:
                # If it ain'tn't bettah, swag that old square back and incr tries
                currSolution[rectNum] = oldRect
                tries += 1
        if currScore > scoreRectangles(bestSolution, refImage):
            bestSolution = copy.deepcopy(currSolution)
            
    finalCanvas = drawRectangles(bestSolution, refImage)
    finalCanvas.show()
    print(score)
    

def drawRectangles(rectangles, refImage):
    width, height = refImage.size
    canvas = Image.new('LA', (width, height), (255))
    
    draw = ImageDraw.Draw(canvas)
    for rect in rectangles:
        draw.rectangle(rect, fill='#123')
    return canvas

def generateRectangles(canvas, numRects):
    rectangles = []
    for i in range(numRects):
        #canvasDrawing.rectangle(generateRectangle(canvas), fill='#124')
        rectangles += [generateRectangle(canvas)]

    return rectangles

def generateRectangle(canvas):
    # Generates a square within the bounds of the canvas
    width, height = canvas.size
    # Generate a random point in the bounds
    x = random.randint(0, width)
    y = random.randint(0, height)
    # generate a random size
    sideLength = random.randint(2, 20)
    return [x, y, x+sideLength, y+sideLength]
    


def hillClimbing(numShapes, timeLimit, minSquareSize, maxSquareSize, canvas):
    size = canvas.size
    startTime = time.time()
    bestSolution= None
    while(time.time() - startTime < timeLimit):
        shapes = randomShapes(numShapes, minSquareSize, maxSquareSize)
        if(bestSolution == None):
            bestSolution = copy.deepcopy(shapes)

        tries = 0
        climbNum = 0
        while(tries < 100 and time.time() - startTime < timeLimit):
            climbNum += 1
            print(climbNum)
            location = random.randrange(0, numShapes)
            
            oldShape = shapes[location]
            shapes[location] = generateShape(canvas)
            score = scoreShapes(shapes, canvas)
            
def scoreRectangles(rectangles, refImage):
    width, height = refImage.size
    #canvas = Image.new('LA', (width, height), (255))
    canvas = drawRectangles(rectangles, refImage)
    return scoreImages(canvas, refImage)

def scoreImages(boxImage, referenceImage):
    s = 0
    for band_index, band in enumerate(boxImage.getbands()):
        m1 = numpy.array([p[band_index] for p in boxImage.getdata()]).reshape(*boxImage.size)
        m2 = numpy.array([p[band_index] for p in referenceImage.getdata()]).reshape(*referenceImage.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s



            


main()
