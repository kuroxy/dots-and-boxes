import time
from playergame import dotsandboxes
from reinforcement import Agent
from utils import plotLearning
import numpy as np
import sys


if __name__ == '__main__':
    # python main.py neuralnetfolder, new, learn, iteration


    begintime=time.time()
    env = dotsandboxes("v5")    #

    n_games = 10

    for i in range(n_games):
        winner = 0
        score = 0
        done = False
        observation = env.reset()

        while not done:
            env.render()
            action = int(input())
            observation_, reward, done, info = env.step(action)

            score += reward
            observation = observation_
        print("winner is ", env.thewinner)
