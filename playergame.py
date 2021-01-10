import utils
import numpy as np
import random
from reinforcement import Agent



class dotsandboxes():
    SIZEX = 5
    SIZEY = 5

    ENVIRONMENT_SHAPE = [(SIZEX+1)*SIZEY+(SIZEY+1)*SIZEX + 2,1,1]
    ACTION_SPACE = [i for i in range((SIZEX+1)*SIZEY+(SIZEY+1)*SIZEX)]
    ACTION_SPACE_SIZE = len(ACTION_SPACE)

    REWARD_NOT_DEAD = 0
    REWARD_WIN = 200
    PUNISHMENT_TIE = -200
    PUNISHMENT_LOSS = -400
    REWARD_BLOCK = 20
    PUNISHMENT_BLOCK = -20

    def __init__(self, botfolder=None):
        self.bot = 0
        if botfolder==None:
            self.bot = Agent(gamma=0.99, epsilon=1.0, alpha=0.001, n_actions=dotsandboxes.ACTION_SPACE_SIZE, input_dims=[dotsandboxes.ACTION_SPACE_SIZE],mem_size=100000, batch_size=64)
        else:
            self.bot = Agent(gamma=0.99, epsilon=0.01, alpha=0.001, n_actions=dotsandboxes.ACTION_SPACE_SIZE, input_dims=[dotsandboxes.ACTION_SPACE_SIZE],mem_size=100000, batch_size=64, chkpt_dir=botfolder)
            self.bot.load_models()


        self.current_state = self.reset()


    def reset(self):
        self.screen = utils.window((dotsandboxes.SIZEX*2+1,dotsandboxes.SIZEY*2+1))

        self.score = [0,0]
        self.moves = 0
        self.thewinner = 0

        self.linesX = [[0 for _ in range(dotsandboxes.SIZEY)] for _ in range(dotsandboxes.SIZEX + 1)]
        self.linesY = [[0 for _ in range(dotsandboxes.SIZEY + 1)] for _ in range(dotsandboxes.SIZEX)]


        return self.observation()

    def observation(self):
        avlist = []
        for i in self.linesX:
            for val in i:
                avlist.append(val)

        for i in self.linesY:
            for val in i:
                avlist.append(val)
        return np.asarray(avlist, dtype=np.float32)

    def step(self, action):
        reward = 0
        currentreward, nextreward, gotpoint, isdone = self.doaction(action, 0)
        reward += currentreward

        if isdone:
            observation_ = self.observation()
            return observation_, reward, isdone, {}

        if not gotpoint:
            gotpoint = True
            while gotpoint:
                gotpoint = False
                botobservation = self.observation()
                action = self.bot.choose_action(botobservation)
                currentreward, nextreward, gotpoint, isdone = self.doaction(action, 1)
                reward += nextreward

        observation_ = self.observation()
        return observation_, reward, isdone, {}


    def actiontopos(self, action):
        x,y,type = 0,0,0    # x: xpos, y: ypos, type: horizontal or vertical

        # going from action to position on the board
        if action >= (dotsandboxes.SIZEX+1)*dotsandboxes.SIZEY:
            action -=  (dotsandboxes.SIZEX+1)*dotsandboxes.SIZEY
            x = action % (dotsandboxes.SIZEX )
            y = int(action / (dotsandboxes.SIZEX))

            type = 1
        else:
            x = action % (dotsandboxes.SIZEX+1)
            y = int(action / (dotsandboxes.SIZEX+1))
            type = 0

        return [x,y,type]


    def checkwinstate(self):
        return self.score[0]+self.score[1] == dotsandboxes.SIZEX*dotsandboxes.SIZEY


    def checkboxes(self,x,y):
        try:
            return self.linesX[x][y] and self.linesX[x + 1][y] and self.linesY[x][y] and self.linesY[x][y + 1]
        except:
            return False


    def setxline(self,x,y, playerturn=-1):
        self.linesX[x][y] = 1
        xpix = x*2
        ypix = y*2+1
        if playerturn == 0:
            self.screen.setpixel((xpix,ypix),"| ", 1)
        elif playerturn ==1:
            self.screen.setpixel((xpix,ypix),"| ", 2)
        else:
            self.screen.setpixel((xpix,ypix),"| ", 9)


        points = 0

        if x-1 >= 0 and x-1 < dotsandboxes.SIZEX:
            points += self.checkboxes(x-1,y)

        if x >= 0 and x+1 < dotsandboxes.SIZEX:
            points += self.checkboxes(x,y)

        return points


    def setyline(self,x,y, playerturn=-1):
        self.linesY[x][y] = 1
        xpix = x*2+1
        ypix = y*2
        if playerturn == 0:
            self.screen.setpixel((xpix,ypix),"--", 1)
        elif playerturn ==1:
            self.screen.setpixel((xpix,ypix),"--", 2)
        else:
            self.screen.setpixel((xpix,ypix),"--", 9)

        points = 0

        if y-1 >= 0 and y-1 < dotsandboxes.SIZEY:
            points += self.checkboxes(x,y-1)

        if y >= 0 and y < dotsandboxes.SIZEY:
            points += self.checkboxes(x,y)

        return points


    def doaction(self, action, playerturn):
        self.moves +=1
        tempcurrentreward = 0
        tempnextreward = 0 # for otherplayer
        tempscore = 0
        x,y,type = self.actiontopos(action)
        lost= False

        if type:# y lines
            if not self.linesY[x][y]:
                points = self.setyline(x,y,playerturn)
                tempscore += points
                tempcurrentreward += points*dotsandboxes.REWARD_BLOCK
                tempnextreward += points*dotsandboxes.PUNISHMENT_BLOCK
            else:
                lost = True

        else:# x lines
            if not self.linesX[x][y]:
                points = self.setxline(x,y,playerturn)
                tempscore += points
                tempcurrentreward += points*dotsandboxes.REWARD_BLOCK
                tempnextreward += points*dotsandboxes.PUNISHMENT_BLOCK
            else:
                lost = True

        self.score[playerturn] += tempscore

        isdone = self.checkwinstate()
        if isdone:
            print("someone has won")
            if self.score[0] > self.score[1]:
                self.thewinner = 1
                if playerturn == 0:                                                         # current player win
                    tempcurrentreward+= dotsandboxes.REWARD_WIN
                    tempnextreward += dotsandboxes.PUNISHMENT_LOSS
                else:                                                                       # other player wins
                    tempcurrentreward+= dotsandboxes.PUNISHMENT_LOSS
                    tempnextreward += dotsandboxes.REWARD_WIN

            elif self.score[0] < self.score[1]:
                self.thewinner = -1
                if playerturn == 1:                                                         # current player win
                    tempcurrentreward+= dotsandboxes.REWARD_WIN
                    tempnextreward += dotsandboxes.PUNISHMENT_LOSS
                else:                                                                       # other player wins
                    tempcurrentreward+= dotsandboxes.PUNISHMENT_LOSS
                    tempnextreward += dotsandboxes.REWARD_WIN

            else:
                self.thewinner = 0                                                                   # draw
                tempcurrentreward+= dotsandboxes.PUNISHMENT_TIE
                tempnextreward += dotsandboxes.PUNISHMENT_TIE   # rewards end of game

        if lost:
            if playerturn == 1:
                self.thewinner = 1

            else:
                self.thewinner = -1
            tempcurrentreward += dotsandboxes.PUNISHMENT_LOSS
            tempnextreward += dotsandboxes.REWARD_WIN
            isdone = True
        else:
            tempcurrentreward += dotsandboxes.REWARD_NOT_DEAD

        return tempcurrentreward, tempnextreward,tempscore!=0, isdone


    def render(self): # drawing screen
        for j in range(dotsandboxes.SIZEY+1):
            for i in range(dotsandboxes.SIZEX+1):
                self.screen.setpixel((i*2,j*2),"* ", 6)


        self.screen.drawscreen()
        print(self.score)
        #self.screen.clearbuffer("  ")
