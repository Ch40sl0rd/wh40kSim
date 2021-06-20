from simulation import Simulation
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def init_argparse()->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description = 'Simulates expected damage output of \
                                     chosen attacker against target using weapon')
    parser.add_argument('-a', '--attacker', default='./database/attacker.csv', help='attacking unit')
    parser.add_argument('-t', '--target', default='./database/target.csv', help='targeted unit')
    parser.add_argument('-w', '--weapon', default='./database/weapon.csv', help='weapon used to do the attack')
    parser.add_argument('-n', '--num-sims', default=10000, type=int, help='Number of simulation runs')
    parser.add_argument('-o','--output', default='damage_output.txt', help='File for calculated damage output')
    return parser

def main():
    parser = init_argparse()
    dict_args = vars(parser.parse_args())
    
    sim = Simulation.from_csv_datafiles(dict_args['attacker'], dict_args['target'], dict_args['weapon'])
    
    damage = sim.simulate_attack_sequence(dict_args['num_sims'])
    fig = sim.visualize_data(damage)
    params, errors = sim.analyze_data(damage)
    sim.visualize_fit(params, fig)
    fig.legend()
    plt.show()

if __name__ == '__main__':
    main()