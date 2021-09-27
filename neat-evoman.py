"""
evoman algorithm using neat. Based on example given here:
https://neat-python.readthedocs.io/en/latest/xor_example.html
"""

# import neat

from __future__ import print_function
import os
import neat
import NEAT.visualize as visualize
import pygame


# imports framework
import sys
sys.path.insert(0, 'evoman')

from NEAT.player_controller import player_controller

from environment import Environment

# imports other libs
import time
import numpy as np
from math import fabs,sqrt
import glob

# parameters:
n_generations = 3
headless = True
should_visualize = True

# choose this for not using visuals and thus making experiments faster
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


experiment_name = 'neat_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# initializes simulation in individual evolution mode, for single static enemy.


env = Environment(experiment_name=experiment_name,
                  enemies=[2],
                  playermode="ai",
                  player_controller=player_controller(),
                  enemymode="static",
                  level=2,
                  speed="fastest")

# default environment fitness is assumed for experiment

env.state_to_log() # checks environment state

####   Optimization for controller solution (best genotype-weights for phenotype-network): Ganetic Algorihm    ###

ini = time.time()  # sets time marker

def simulation(pcont):
    f, _ , _ ,_ = env.play(pcont=pcont)
    return f

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        pcont = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = simulation(pcont)


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Determine number of generations
    winner = p.run(eval_genomes, n_generations)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    #winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    print("To do, print output configuration here")

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'} #example of node names from xor problem

    if should_visualize:
        # try implementing the visualisation of the winning network
        visualize.draw_net(config, winner, True, node_names=None)
        visualize.plot_stats(stats, ylog=False, view=True)
        visualize.plot_species(stats, view=True)

    ## runs can be restored from checkpoints as follows:
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 1)

#
#
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    print("local dir:", local_dir)
    config_path = os.path.join(local_dir, 'NEAT/config_neat')
    run(config_path)