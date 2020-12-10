import pygal
import numpy as np


def plotLearning(x, scores, epsilons, filename, lines=None):
                                                     # First import pygal
    line_chart = pygal.Line()
    line_chart.title = 'reinforcement'
    line_chart.x_labels = x
    line_chart.add('scores', scores)
    line_chart.add('epsilons',  [i*100 for i in epsilons])
    line_chart.render_to_png('chart.png')      # Save the svg to a file
