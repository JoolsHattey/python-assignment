# Python Assignment: A Patchwork Sampler
# UP894547

from graphics import *

## Drawing Patch Shapes ##


def drawCircle(coords, radius, colour, win, fill):
    circle = Circle(coords, radius)
    if fill:
        circle.setFill(colour)
    circle.setOutline(colour)
    circle.draw(win)


def drawTriangle(coord1, coord2, coord3, colour, win):
    triangle = Polygon(coord1, coord2, coord3)
    triangle.setFill(colour)
    triangle.setOutline(colour)
    triangle.draw(win)


def draw2TrianglesDown(x, y, colour, win):
    drawTriangle(Point(x, y), Point(x+20, y), 
                Point(x+10, y+10), colour, win)
    drawTriangle(Point(x, y+10), Point(x+20, y+10), 
                Point(x+10, y+20), colour, win)


def draw2TrianglesRight(x, y, colour, win):
    drawTriangle(Point(x, y), Point(x+10, y+10), 
                Point(x, y+20), colour, win)
    drawTriangle(Point(x+10, y), Point(x+20, y+10), 
                Point(x+10, y+20), colour, win)


## Drawing Patch ##
    
def drawPatchF(x, y, colour, win):
    for i in range(0, 10):
        drawCircle(Point(50 + x, 50+ i*5 + y), 50 - i*5, 
                                                colour, win, False)


def drawPatchP(x, y, colour, win):
    for a in range(0, 3):
        for b in range(0, 2):
            drawCircle(Point(x + b*40 + 30, y + a*40 + 10), 10, 
                                                colour, win, True)
    for a in range(0, 2):
        for b in range(0,3):
            drawCircle(Point(x + b*40 + 10, y + a*40 + 30), 10, 
                                                colour, win, True)
    for a in range(0, 3):
        for b in range(0, 3):
            draw2TrianglesDown(x + a*40, y + b*40, colour, win)
    for a in range(0, 2):
        for b in range(0, 2):
            draw2TrianglesRight(x + a*40 + 20, y + b*40 + 20, colour, win)


## Drawing patches on the window ##

def drawPatchWork(colours, win, size):
    for a in range(0, 2):
        for b in range(0, 4-a+size):
            drawPatchP(b*100, a*100, colours[0], win)
    for a in range(0, 2+size):
        for b in range(0, 2-a+size):
            drawPatchF(b*100, a*100+200, colours[0], win)
    for a in range(0, 3+size):
        drawPatchF(a*100, 400+size*100 - a*100, colours[1], win)
    for a in range(0, 2+size):
        for b in range(0, 2-a+size):
            drawPatchF(b*100 + (a*100+100), 400+size*100 - a*100, 
                                                    colours[2], win)
    for a in range(0, 2):
        for b in range(0, (3+size)+a):
            drawPatchP(300+size*100 + a*100, 400+size*100 - b*100, 
                                                    colours[2], win)
    for a in range(0, 2):
        drawPatchP(300+size*100 + a*100, 100 - a*100, colours[1], win)


## Edit Patch ##
    
def modifyPatch(win, selection, mode):
    x1 = selection.getP1().getX()
    y1 = selection.getP1().getY()
    x2 = selection.getP2().getX()
    y2 = selection.getP2().getY()
    empty = True
    type = "F"
    colour = ""
    # Iterates through each item in the window
    for item in win.items[:]:
        try:
            # Checks if the coordinates are within the selection
            # Trys to get the list point values of the item
            points = item.getPoints()
            if (points[2].getX() > x1 and points[2].getY() > y1 
            and points[2].getX() <=x2 and points[2].getY() <= y2):
                if item != selection:
                    empty = False
                    colour = item.config["outline"]
                if mode == "delete" and item != selection:
                    item.undraw()
                type = "P"
        except AttributeError:
            try:
                # If this fails it will get the P1 value of the item
                itemX1 = item.getP1().getX()
                itemY1 = item.getP1().getY()
                if (itemX1 >= x1 and itemX1 < x2 
                and itemY1 >= y1 and itemY1 < y2):
                    if item != selection:
                        empty = False
                        colour = item.config["outline"]
                    if mode == "delete" and item != selection:
                        item.undraw()
            except AttributeError:
                pass
    win.update()
    if mode == "checkContents":
        return empty
    if mode == "checkType":
        return type, colour


def switchPatch(win, selection):
    # Checks the type of patch and switched the the opposite type
    patch, colour = modifyPatch(win, selection, "checkType")
    if patch == "P":
        modifyPatch(win, selection, "delete")
        drawPatchF(selection.getP1().getX(), selection.getP1().getY(),
                                                            colour, win)
    if patch == "F":
        modifyPatch(win, selection, "delete")
        drawPatchP(selection.getP1().getX(), selection.getP1().getY(), 
                                                            colour, win)


def drawPatchInEmptySpace(win, selection, colour):
    if modifyPatch(win, selection, "checkContents"):
        drawPatchF(selection.getP1().getX(), selection.getP1().getY(), 
                                                            colour, win)


def getKeyPress(win, selection):
    x = True  
    while x:
        key = win.getKey()
        if key == "d":
            modifyPatch(win, selection, "delete")
        if key == "s":
            switchPatch(win,selection)
        if key == "r":
            drawPatchInEmptySpace(win, selection, "red")
        if key == "g":
            drawPatchInEmptySpace(win, selection, "green")
        if key == "b":
            drawPatchInEmptySpace(win, selection, "blue")
        if key == "m":
            drawPatchInEmptySpace(win, selection, "magenta")
        if key == "o":
            drawPatchInEmptySpace(win, selection, "orange")
        if key == "p":
            drawPatchInEmptySpace(win, selection, "pink")
        if key == "Return":
            selection.undraw()
            break


def selectPatch(win):
    mouse = win.getMouse()
    x = int(mouse.getX())
    y = int(mouse.getY())
    if x < 100:
        x = 0
    else:
        x = int(str(x)[:1]) * 100
    if y < 100:
        y = 0
    else:
        y = int(str(y)[:1]) * 100
    selection = Rectangle(Point(x,y), Point(x+100, y+100))
    selection.setOutline("black")
    selection.draw(win)
    return selection
    
def editPatch(win):
    while True:
        selection = selectPatch(win)
        getKeyPress(win, selection)


## User Interface ##
 

def choosePatchColour():
    validColours = ["red", "green", "blue", "magenta", "orange", "pink"]
    colours = ["", "", ""]
    print("Enter patch colours.")
    for i in range (0, 3):
        while (colours[i] in validColours) == False:
            colours[i] = input("Patch colour " + str(i + 1) + ": ")
            if (colours[i] in validColours) == False:
                print("Invalid Colour. Enter a valid colour.")
    return colours
   

def choosePatchSize():
    print("Enter patch size")
    print("Valid sizes are 5 7 or 9")
    validSizes = [5, 7, 9]
    size = 0
    while (size in validSizes) == False:
        size = int(input("Patch size: "))
        if (size in validSizes) == False:
            print("Invalid Size. Enter a valid size.")
    return size
    print("")


def main():
    print("Patchwork Sampler. UP894547.\n")
    size = choosePatchSize()
    colours = choosePatchColour()
    win = GraphWin("Patchwork Sampler", size*100, size*100)
    drawPatchWork(colours, win, size-5)
    editPatch(win)
 

main()