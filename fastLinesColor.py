from PIL import Image
import random, time, copy, math, sys
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
    return int(round(255/(math.exp(float(weight)/2)), 0))            

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

def fastDrawLinesColor(lines, matrix, xSize, ySize):
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

def getError(img, matrix, x, y):
    return abs(weightMap(matrix[y][x]) - getPixel(img, x, y))
                
def calcError(img, matrix, xSize, ySize):
    error = 0
    for y in range(ySize):
        for x in range(xSize):
            error += getError(img, matrix, x, y)
    return error

#adds a line and returns the change in total error that this action results in
def addLine(line, matrix, image, xSize, ySize):
    change = 0
    if(line[3] == 0): #(m, x0, y0, inverted)
        #not inverted
        for x in range(xSize): # y = m(x-x0) + y0
            y = int(round((x - line[1])*line[0] + line[2], 0))
            if(y >= 0 and y < ySize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] += 1
                change += getError(image, matrix, x, y) - oldErr
    else:
        #inverted
        for y in range(ySize): # x = m(y - y0) + x0
            x = int(round((y - line[2])*line[0] + line[1], 0))
            if(x >= 0 and x < xSize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] += 1
                change += getError(image, matrix, x, y) - oldErr
    return change

#adds a line and returns the change in total error that this action will results in
def removeLine(line, matrix, image, xSize, ySize):
    change = 0
    if(line[3] == 0): #(m, x0, y0, inverted)
        #not inverted
        for x in range(xSize): # y = m(x-x0) + y0
            y = int(round((x - line[1])*line[0] + line[2], 0))
            if(y >= 0 and y < ySize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] = max(matrix[y][x] - 1, 0)
                change += getError(image, matrix, x, y) - oldErr
    else:
        #inverted
        for y in range(ySize): # x = m(y - y0) + x0
            x = int(round((y - line[2])*line[0] + line[1], 0))
            if(x >= 0 and x < xSize):
                oldErr = getError(image, matrix, x, y)
                matrix[y][x] = max(matrix[y][x] - 1, 0)
                change += getError(image, matrix, x, y) - oldErr
    return change
    
def drawMatrix(matrix, xSize, ySize, lines):
    image = Image.new('RGB', (xSize, ySize))
    for y in range(ySize):
        for x in range(xSize):
            image.putpixel((x, y), (255, 255, 255))
    for line in lines:
        
        if(line[3] == 0): #(m, x0, y0, inverted)
                #not inverted
                for x in range(xSize): # y = m(x-x0) + y0
                    y = int(round((x - line[1])*line[0] + line[2], 0))
                    if(y >= 0 and y < ySize):
                        image.putpixel((x, y), line[4])
        else:
                #inverted
                for y in range(ySize): # x = m(y - y0) + x0
                    x = int(round((y - line[2])*line[0] + line[1], 0))
                    if(x >= 0 and x < xSize):
                        image.putpixel((x, y), line[4])
            
    image.show()

def hillClimbing(path, numLines, timeLimit):
    #setup
    img = Image.open(path)
    xSize, ySize = img.size
    img.draft('L', img.size)
    
    matrix = list()
    startTime = time.time()
    bestLines = []
    bestSolution = None
    bestScore = None
    #keep searching for solution while there is time last
    while(time.time() - startTime < timeLimit):
        #randomly draw lines
        initMatrix(matrix, xSize, ySize)
        lines = randomizeLines(numLines, xSize, ySize)
        fastDrawLines(lines, matrix, xSize, ySize)
        error = calcError(img, matrix, xSize, ySize)
        if(bestSolution == None):
            bestSolution = copy.deepcopy(matrix)
            bestScore = error
        count = 0
        bestLines = copy.deepcopy(lines)
        while(time.time() - startTime < timeLimit):
            #pick a random line and make it something else
            index = random.randrange(numLines)
            oldLine = lines[index]
            newLine = getRandLine(xSize, ySize)

            #change the line and get new score
            change = removeLine(oldLine, matrix, img, xSize, ySize)
            change += addLine(newLine, matrix, img, xSize, ySize)
            #check that the move is an improvement
            if(change < 0):
                #if it is, keep it
                lines[index] = newLine
                error += change

                bestLines = copy.deepcopy(lines)
            else:
                #if not, switch the line back
                removeLine(newLine, matrix, img, xSize, ySize)
                addLine(oldLine, matrix, img, xSize, ySize)
            count += 1
            sys.stdout.write("\r" + str(count) + ": " + str(error) + " -- " + "{0:.1f}".format(timeLimit- (time.time()-startTime)))
            sys.stdout.flush()
        #if the new solution is better that the old best solution, replace the old best
        if(error < bestScore):
            bestSolution = copy.deepcopy(matrix)
            bestScore = error
    print("")
    return (bestSolution, xSize, ySize, bestLines)

def colorize(lines, imagePath):
    refImage = Image.open(imagePath)
    xSize, ySize = refImage.size

    newLines = []
    for line in lines:
        # Compute the average RGB value of pixels on this line
        # Go through the refImage and collect the pixels on the given line
        r = 0
        g = 0
        b = 0
        pixels = 0
        if(line[3] == 0): #(m, x0, y0, inverted)
            #not inverted
            for x in range(xSize): # y = m(x-x0) + y0
                y = int(round((x - line[1])*line[0] + line[2], 0))
                if(y >= 0 and y < ySize):
                    r1, g1, b1 = refImage.getpixel((x, y))
                    r += r1
                    g += g1
                    b += b1
                    pixels += 1
        else:
            #inverted
            for y in range(ySize): # x = m(y - y0) + x0
                x = int(round((y - line[2])*line[0] + line[1], 0))
                if(x >= 0 and x < xSize):
                    r1, g1, b1 = refImage.getpixel((x, y))
                    r += r1
                    g += g1
                    b += b1
                    pixels += 1
        rgb = (int(r/pixels), int(g/pixels), int(b/pixels))
        newLines += [[line[0], line[1], line[2], line[3], rgb]]
        
    return newLines

    
def main():
    args = sys.argv
    if(len(args) < 4):
        print("Usage: python " + args[0] + " [image path] [num lines] [time]")
        return
    result = hillClimbing(args[1], int(args[2]), int(args[3]))
    colored = colorize(result[3], args[1])
    matrix = []
    initMatrix(matrix, result[1], result[2])
    fastDrawLinesColor(colored, matrix, result[1], result[2])
    drawMatrix(matrix, result[1], result[2], colored)
main()
