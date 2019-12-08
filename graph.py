import random
from tkinter import *
from ast import literal_eval
import csv

#File format required:
#csv file
#csv file format: user, label, tuples containing ratios
#tuple format: (topleft, bottomleft, topright, bottomright)

#example line in csv file:
#User1234, Braincels, (1, 0, 0, 0), (0.5, 0.25, 0.25, 0), NULL, (0.22, 0.22, 0.22, 0.34), ...

FILE="ToxicVsParentToxic2.csv" #file containing data to visualize
FILE2 = "PoliticsToxicVsNumPoliticsComments.csv"
FILE3 = "PoliticsToxicVsParentPolitics2.csv"
FILE4 = "ClassifiedUsers/ALLToxicVsParentALL2.csv"
FILE3 = "ClassifiedUsers/politicsall.csv"
FILE4 = "ClassifiedUsers/politicsInvsIn.csv"
FILE5 = "ClassifiedUsers/politicsOutvsOut.csv"


FILE6 ="ClassifiedUsers/incelsall.csv"
FILE7 ="ClassifiedUsers/incelsInvsIn.csv"
FILE8 ="ClassifiedUsers/incelsOutvsOut.csv"

FILE9 ="ClassifiedUsers/donaldall.csv"
FILE10 ="ClassifiedUsers/donaldInvsIn.csv"
FILE11 ="ClassifiedUsers/donaldOutvsOut.csv"

FILE12 ="ClassifiedUsers/gamingall.csv"
FILE13 ="ClassifiedUsers/gamingInvsIn.csv"
FILE14 ="ClassifiedUsers/gamingOutvsOut.csv"

FILE15 ="ClassifiedUsers/mademesmileall.csv"
FILE16 ="ClassifiedUsers/mademesmileInvsIn.csv"
FILE17 ="ClassifiedUsers/mademesmileOutvsOut.csv"

FILE18 = "ClassifiedUsers/politicsratio.csv"
FILE19 = "ClassifiedUsers/incelsratio.csv"
FILE20 = "ClassifiedUsers/donaldratio.csv"
FILE21 = "ClassifiedUsers/gamingratio.csv"
FILE22 = "ClassifiedUsers/mademesmileratio.csv"

TOPLEFTLABEL= "Toxicity" #label of top left corner
# TOPRIGHTLABEL= "other" # label of top right corner
# BOTTOMLEFTLABEL= "mgtow" #label of bottom left corner
BOTTOMRIGHTLABEL= "Affinity" #label of bottom right corner
TIMEFRAME= "Months" #is the timestep a month? a week?

DOTCOLORS= {"suspect":"red", "":"blue"} #color of dots based on label
LINECOLORS= {"suspect":"salmon", "":"light blue"} #color of lines based on label
SPEED= 30 #higher number means slower
LEN=6


def preprocess(data):
    #ff = open("incels_ratio_snapshot.csv", "w")
    #csvwriter = csv.writer(ff)
    with open(FILE19, encoding="utf-8") as readfile:
        csvreader = csv.reader(readfile)
        for line in csvreader:
            rowx = []
            rowy = []
            braincel=False
            if(len(line) == 0 or line[0] == ""):
                continue
            #if(line[1] != "suspect"):
                #continue
            # if(len(line) != 8):
            #     continue
            for i in range(2, len(line)):
                data.length = len(line)-2
                tup = line[i]

                if(tup[0] != "(" and i == 2):
                    rowx.append(50)
                    rowy.append(data.height-50)
                elif(tup[0] != "("):
                    #print(tup)
                    rowx.append("Null")
                    rowy.append("Null")
                else:
                    #(braincels=0,0, incels=1,1, mgtow=0,1, other=1,0)

                    t = tup[1:-1]
                    t = t.split(",")
                    new_t = []

                    for num in t:
                        new_t.append(float(num))
                    if(new_t[0] > 0):
                        braincel=True
                    w = 0#0(data.width-100)
                   # print(w)
                    h = (data.height-100)
                    xb = (data.width - 100)*new_t[1]
                    yb = 0#-h*new_t[0]

                    xi =0#data.width - 100)*new_t[1]
                    yi = -h*new_t[0]

                    #xm = w*new_t[2]
                    #ym = 0#-h*new_t[2]

                    #xo = 0#w*new_t[3]
                    #yo = h*new_t[3]
                    xcoords = [xb, xi]
                    ycoords = [yb, yi]
                    
                    x = xb+xi
                    y = yb+yi

                    x = w + x +50
                    y = h +y+50

                    rowx.append(x)
                    rowy.append(y)
            color = DOTCOLORS[line[1]]
            linecolor = LINECOLORS[line[1]]
            data.dots.append(Dot(rowx[0], rowy[0], color,linecolor, rowx, rowy, data))
            # if(rowx[0] != "Null" and rowy[0] != "Null"):
            #     csvwriter.writerow([rowx[0]/data.width, rowy[0]/data.height])
            #print(rowx, rowy)
    #print(len(data.dots))


class Line(object):
    def __init__(self, x0, y0, x1, y1, color):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.color = color
        self.line = None
        self.width=0.1
    def draw(self, canvas):
        self.line = canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.color, width=self.width)

    def updateLine(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

class Dot(object):
    dotCount = 0

    def __init__(self, x, y, color,linecolor,  xlist, ylist, data):
        Dot.dotCount += 1
        self.x = x
        self.y = y

        self.x_list = xlist
        self.y_list = ylist
        self.r = 2.5
        self.fill = color
        self.linecolor=linecolor
        self.clickCount = 0
        self.xspeed = 0
        self.yspeed = 0
        self.lines = []
        self.dot = None
        self.prev_count = -1


    def draw(self,data,  canvas):
        #if(self.x_list[data.count] !="Null"):
            self.dot = canvas.create_oval(self.x-self.r, self.y-self.r,
                               self.x+self.r, self.y+self.r,
                               fill=self.fill)
            if(self.x==data.width-50 and self.y==data.height-50):
                data.incel+=1
            elif((self.x==50 and self.y==data.height-50)):
                data.mgtow+=1
            elif((self.y==50 and self.x==data.width-50)):
                data.other+=1
            elif(self.x==50 and self.y==50):
                data.braincel+=1
        # else:
        #     self.dot=None
       

    def addLine(self, data):
        new_line = Line(self.x, self.y, self.x, self.y, self.linecolor)
        self.lines.append(new_line)
        data.lines.append(new_line)
        if(len(data.lines) > len(data.dots)):
            data.lines.pop(0)

    def onTimerFired(self, data):
        if(LEN==1):return
        if(self.x_list[data.count] =="Null"):
            return
        
        if data.count != self.prev_count:
            self.addLine(data)
            self.prev_count = data.count

            self.xspeed = (self.x_list[data.count] - self.x)/data.steps
            self.yspeed = (self.y_list[data.count] - self.y)/data.steps

        self.x += self.xspeed
        self.y += self.yspeed
        if(len(self.lines)>0):
            self.lines[-1].updateLine(self.x, self.y)





def init(data):
    
    data.dots = [ ]
    data.lines = [ ]
    preprocess(data)
    data.cur_steps = 0



def redrawAll(canvas, data):
    
    for line in data.lines:
        line.draw(canvas)
    for dot in data.dots:
        dot.draw(data, canvas)
    t0 = canvas.create_text(data.width/2, 10, text=TIMEFRAME+" %d" % data.count, anchor = 'n')
    t1 = canvas.create_text(20, 20, text=TOPLEFTLABEL, anchor = "nw")
    t2 = canvas.create_text(data.width, data.height-10, text=BOTTOMRIGHTLABEL, anchor = "se")
    #t3 = canvas.create_text(data.width-5, data.height/2, text=TOPRIGHTLABEL+": %d" %data.other, anchor="e")
    #t4 = canvas.create_text(5, data.height/2, text=BOTTOMLEFTLABEL+": %d" %data.mgtow, anchor="w")
    data.texts = [t0, t1, t2]

def keyPressed(event, data):
    pass

def timerFired(data):
    data.mgtow=0
    data.braincel=0
    data.incel=0
    data.other=0
    data.steps = SPEED
    if data.cur_steps % data.steps == 0:
        if(data.count < LEN):
            data.count += 1
    if(data.cur_steps/data.steps < LEN):
        for dot in data.dots:
            dot.onTimerFired(data)
    data.cur_steps+=1
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        for dot in data.dots:
            if(dot.dot != None):
                canvas.delete(dot.dot)
        for line in data.lines:
            canvas.delete(line.line)
        for t in data.texts:
            canvas.delete(t)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.texts = []
    data.count = 0
    data.timerDelay = 50 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700, 700)