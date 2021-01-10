import os

class window():
    def __init__(self,winsize):
        self.winsize=tuple(winsize)
        self.buffer = None
        self.clearbuffer("  ")
        self.clear = "clear"
        if os.name=="nt":
            self.clear="cls"

    def drawscreen(self):
        #clear terminal then draw screen
        #os.system(self.clear)

        for i in range(self.winsize[1]):
            print("".join(self.buffer[i]))


    def setpixel(self,pos ,chararcter):
        self.buffer[pos[1]][pos[0]] = chararcter


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

class Environment:
    SIZEX = 5
    SIZEY = 5

    ENVIRONMENT_SHAPE = ((SIZEX+1)*SIZEY+(SIZEY+1)*SIZEX + 2,1,1)
    ACTION_SPACE = [i for i in range((SIZEX+1)*SIZEY+(SIZEY+1)*SIZEX)]
    ACTION_SPACE_SIZE = len(ACTION_SPACE)

    REWARD_WIN = 100
    PUNISHMENT_TIE = -50
    PUNISHMENT_LOSS = -100
    REWARD_BLOCK = 1
    PUNISHMENT_BLOCK = -1

    def __init__(self):
        self.current_state = self.reset()


    def reset(self):
        self.score = [0,0]
        self.winner = False

        self.linesX = [[False for _ in range(Environment.SIZEY)] for _ in range(Environment.SIZEX + 1)]
        self.linesY = [[False for _ in range(Environment.SIZEY + 1)] for _ in range(Environment.SIZEX)]
        return self.observation()


    def step(self, action):
        reward = 0

        x,y,side = 0,0,0
        index = action

        if index >= (Environment.SIZEX+1)*Environment.SIZEY:
            index -=  (Environment.SIZEX+1)*Environment.SIZEY
            x = index % (Environment.SIZEX )
            y = int(index / (Environment.SIZEX))

            side = 1
        else:
            x = index % (Environment.SIZEX+1)
            y = int(index / (Environment.SIZEX+1))
            side = 0

        if side:
            extra = Environment.setyline(x,y)
            if extra == "LOSE":
                reward =+ Environment.PUNISHMENT_LOSS
            else:
                if not extra[0] and not extra[1]:
                    if player:
                        player =0
                    else:
                        player =1
                if extra[0]:
                    score[player] +=1
                if extra[1]:
                    score[player] +=1
        else:
            extra = Environment.setxline(x,y)
            if extra == "LOSE":
                reward =+ Environment.PUNISHMENT_LOSS
            else:
                if not extra[0] and not extra[1]:
                    if player:
                        player =0
                    else:
                        player =1
                if extra[0]:
                    reward =+ Environment.REWARD_BLOCK
                    score[player] +=1
                if extra[1]:
                    reward =+ Environment.REWARD_BLOCK
                    score[player] +=1


        if score[0]+score[1] == Environment.SIZEX*Environment.sizey:
            if score[0] > score[1]:
                print(f"Player 0 won {score[0]} {score[1]}")

                if player == 0:
                    reward =+ Environment.REWARD_WIN
                else:
                    reward =+ Environment.PUNISHMENT_LOSS


            elif score[0] < score[1]:
                print(f"Player 1 won {score[0]} {score[1]}")

                if player == 0:
                    reward =+ Environment.PUNISHMENT_LOSS
                else:
                    reward =+ Environment.REWARD_WIN
            else:
                print(f"Draw {score[0]} {score[1]}")
                reward =+ Environment.PUNISHMENT_TIE



    def checkboxes(self,x,y):
        try:
            return Environment.linesX[x][y] and Environment.linesX[x + 1][y] and Environment.linesY[x][y] and Environment.linesY[x][y + 1]
        except:
            return False


    def setxline(self,x,y):
        if self.linesX[x][y]:
            return "LOST"

        self.linesX[x][y] = True
        points = [0,0]

        if x-1 >= 0 and x-1 < Environment.SIZEX:
            points[0] = self.checkboxes(x-1,y)
        else:
            points[0] = False

        if x+1 >= 0 and x+1 < Environment.SIZEX:
            points[1] = self.checkboxes(x+1,y)
        else:
            points[1] = False

        return points


    def setyline(self,x,y):
        if self.linesY[x][y]:
            return "LOST"

        self.linesY[x][y] = True
        points = [0,0]

        if y-1 >= 0 and y-1 < Environment.SIZEY:
            points[0] = self.checkboxes(x,y-1)
        else:
            points[0] = False

        if y+1 >= 0 and y+1 < Environment.SIZEY:
            points[1] = self.checkboxes(x,y+1)
        else:
            points[1] = False

        return points


    def observation(self):
        avlist = []
        for i in range(linesX):
            for val in i:
                avlist.append(val)

        for i in range(linesY):
            for val in i:
                avlist.append(val)
        return avlist



gamesize = [5,5]
screen = window((gamesize[0]*2+1,gamesize[1]*2+1))
thegame = Environment()
player = 0
score = [0,0]


while True:

    # drawing screen
    for j in range(thegame.SIZEY+1):
        for i in range(thegame.SIZEX+1):
            screen.setpixel((i*2,j*2),"* ")

    for x in range(len(thegame.linesX)):
        for y in range(len(thegame.linesX[x])):
            if thegame.linesX[x][y]:
                xpix = x*2
                ypix = y*2+1
                screen.setpixel((xpix,ypix),"| ")

    for x in range(len(thegame.linesY)):
        for y in range(len(thegame.linesY[x])):
            if thegame.linesY[x][y]:
                xpix = x*2+1
                ypix = y*2
                screen.setpixel((xpix,ypix),"--")


    screen.drawscreen()
    screen.clearbuffer("  ")



    print(score)
    print(player)

    x,y,side = 0,0,0
    index = 0 # get player action
    index = int(input())

    if index >= (thegame.SIZEX+1)*thegame.SIZEY:
        index -=  (thegame.SIZEX+1)*thegame.SIZEY
        x = index % (thegame.SIZEX )
        y = int(index / (thegame.SIZEX))

        side = 1
    else:
        x = index % (thegame.SIZEX+1)
        y = int(index / (thegame.SIZEX+1))
        side = 0

    if side:
        extra = thegame.setyline(x,y)
        if not extra[0] and not extra[1]:
            if player:
                player =0
            else:
                player =1
        if extra[0]:
            score[player] +=1
        if extra[1]:
            score[player] +=1
    else:
        extra = thegame.setxline(x,y)
        if not extra[0] and not extra[1]:
            if player:
                player =0
            else:
                player =1
        if extra[0]:
            score[player] +=1
        if extra[1]:
            score[player] +=1

    if score[0]+score[1] == thegame.SIZEX*thegame.sizey:
        if score[0] > score[1]:
            print(f"Player 0 won {score[0]} {score[1]}")
        elif score[0] < score[1]:
            print(f"Player 1 won {score[0]} {score[1]}")
        else:
            print(f"Draw {score[0]} {score[1]}")
        break
