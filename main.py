from src.simulation import Simulation
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathos.multiprocessing as mp

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

def mp_simulate_attack(sim:Simulation):
    return sim.simulate_attack_sequence()

def run_default_targets(file_at:str, file_wp:str, file_targets:str = 'database/default_targets.csv', n:int=10000):
    def_targets = pd.read_csv(file_targets, skipinitialspace=True)
    attacker = pd.read_csv(file_at, skipinitialspace=True).iloc[0]
    weapon = pd.read_csv(file_wp, skipinitialspace=True).iloc[0]
    num_targets = def_targets.shape[0]
    sims = []
    for i in range(num_targets):
        sims.append(Simulation.from_dataframes(attacker, def_targets.iloc[i], weapon, n))
        
    pool = mp.ProcessPool(num_targets)
    results_dmg = pool.map(Simulation.simulate_attack_sequence, sims)
    
    results_params = pool.map(Simulation.analyze_data, sims, results_dmg)
    for result in results_params:
        print(result)
        
    pool.close()
    pool.join()
    
    
def main():
    parser = init_argparse()
    dict_args = vars(parser.parse_args())
    #print(dict_args)
    
    run_default_targets(dict_args['attacker'], dict_args['weapon'], n=dict_args['num_sims'])

if __name__ == '__main__':
    main()