import pygal
import numpy as np
import os
import colored

def plotLearning(x, scores, avgmoves,avg_winrate, epsilons, filename):                                                 # First import pygal
    line_chart = pygal.Line()
    line_chart.title = 'reinforcement'
    line_chart.x_labels = x
    line_chart.add('scores', scores)
    line_chart.add('moves', avgmoves)
    line_chart.add('winerate', [i*100 for i in avg_winrate])
    line_chart.add('epsilons',  [i*100 for i in epsilons])
    line_chart.render_to_png(filename)      # Save the png to a file

class window():
    def __init__(self,winsize):
        self.winsize=tuple(winsize)
        self.buffer = None
        self.colorbuffer = None
        self.clearbuffer()
        self.clearcolorbuffer()
        self.clear = "clear"
        if os.name=="nt":
            self.clear="cls"

    def drawscreen(self):
        #clear terminal then draw screen
        #os.system(self.clear)
        for i in range(self.winsize[1]):
            for j in range(self.winsize[0]):
                print(colored.fg(self.colorbuffer[i][j]) + self.buffer[i][j] + colored.fg("white"), end="")
            print()


    def setpixel(self,pos ,chararcter, color=9):
        self.buffer[pos[1]][pos[0]] = chararcter
        self.colorbuffer[pos[1]][pos[0]] = color


    def setpixels(self,pos1,pos2,chararcter):

        if pos1[0] == pos2[0]:
            for y in range(pos1[1],pos2[1]+1):
                self.setpixel((pos1[0],y), chararcter)
        elif pos1[1]==pos2[1]:

            for x in range(pos1[0],pos2[0]+1):
                self.setpixel((x,pos1[1]), chararcter)
        else:
            for y in range(pos1[1],pos2[1]+1):
                for x in range(pos1[0],pos2[0]+1):
                    self.setpixel((x,y), chararcter)


    def clearbuffer(self, chararcter="  "):
        self.buffer = [[chararcter for _ in range(self.winsize[0])] for _ in range(self.winsize[1])]

    def clearcolorbuffer(self, color="white"):
        self.colorbuffer = [[color for _ in range(self.winsize[0])] for _ in range(self.winsize[1])]


if __name__=="__main__":
    screen = window((11,11))

    for j in range(5+1):
        for i in range(5+1):
            screen.setpixel((i*2,j*2),"* ", 1)

    for x in range(6):
        for y in range(5):
            xpix = x*2
            ypix = y*2+1
            screen.setpixel((xpix,ypix),"| ",2)

    for x in range(5):
        for y in range(6):

            xpix = x*2+1
            ypix = y*2
            screen.setpixel((xpix,ypix),"--",3)


    screen.drawscreen()
    screen.clearbuffer()
    screen.clearcolorbuffer()
