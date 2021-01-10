import time
from environ import dotsandboxes
from reinforcement import Agent
from utils import plotLearning
import numpy as np
import sys


if __name__ == '__main__':
    # python main.py neuralnetfolder, new, learn, iteration


    botdir = sys.argv[1]

    begintime=time.time()
    env = dotsandboxes("v5")    #
    epsi = .1 if sys.argv[3] =="1" else 0.01
    agent = Agent(gamma=0.99, epsilon=epsi, alpha=0.0001, n_actions=dotsandboxes.ACTION_SPACE_SIZE, input_dims=[dotsandboxes.ACTION_SPACE_SIZE],mem_size=100000, batch_size=64, chkpt_dir=botdir)
    if sys.argv[2] =="0":
        agent.load_models()



    scores, moves, winrate, avg_scores, avg_moves, avg_winrates, eps_history = [],[], [], [], [], [], []
    n_games = int(sys.argv[4])

    for i in range(n_games):
        winner = 0
        score = 0
        done = False
        observation = env.reset()

        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)



            #env.render()
            #time.sleep(1)
            score += reward
            if sys.argv[3] == "1":
                agent.store_transition(observation, action, reward,observation_, done)
                agent.learn()
            observation = observation_


        scores.append(score)
        moves.append(env.moves)
        winrate.append(env.thewinner)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        avg_move =np.mean(moves[-100:])
        avg_winrate = np.mean(winrate[-100:])

        avg_scores.append(avg_score)
        avg_moves.append(avg_move)
        avg_winrates.append(avg_winrate)

        print('epi', i, 'epsilon %.2f' % agent.epsilon, 'score {:<5}'.format(score),'avg_score {:<6}'.format(avg_score),'moves {:<3}'.format(env.moves),'avg_moves {:<6}'.format(avg_move),'winner {:<1}'.format(env.thewinner),'avg_winrate {:<6}'.format(avg_winrate) )

    x = [i+1 for i in range(n_games)]
    filename = f"{botdir}.png"

    if sys.argv[3] == "1":
        agent.save_models()
    print(f"took {time.time()-begintime} seconds")

    if sys.argv[3] == "1":
        plotLearning(x, avg_scores, avg_moves, avg_winrates, eps_history, filename)
