from src.simulation import Simulation
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def init_argparse()->argparse.ArgumentParser:
    '''
    deal with command line arguments. Supported arguments are
        - attacker : choose file for attacker statline
        - target : choose file for target statline
        - weapon : choose file for weapon statline
        - num-sims : number of simulation runs
        - output : choose file for stat output
    '''
    parser = argparse.ArgumentParser(description = 'Simulates expected damage output of \
                                     chosen attacker against target using weapon')
    parser.add_argument('-a', '--attacker', default='./database/attacker.csv', help='attacking unit')
    parser.add_argument('-t', '--target', default='./database/target.csv', help='targeted unit')
    parser.add_argument('-w', '--weapon', default='./database/weapon.csv', help='weapon used to do the attack')
    parser.add_argument('-n', '--num-sims', default=10000, type=int, help='Number of simulation runs')
    parser.add_argument('-o','--output', default='damage_output.txt', help='File for calculated damage output')
    return parser
    
def main():
    pass

if __name__ == '__main__':
    main()