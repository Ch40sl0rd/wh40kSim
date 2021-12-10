import random

from pandas.core.indexes.base import InvalidIndexError
import unit_classes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.odr as odr

class Simulation():
    def __init__(self, attacker, target, weapon, num_runs:int = 10000):
        if (isinstance(attacker, unit_classes.Attacker)==False):
            raise TypeError('selected attacker is not of type attacker')
        if(isinstance(target, unit_classes.Target)==False):
            raise TypeError('selected target is not of type target')
        if(isinstance(weapon, unit_classes.Weapon)==False):
            raise TypeError('selected weapon is not of type weapon')
        self.attacker = attacker
        self.target = target
        self.weapon = weapon
        self.num_runs = num_runs
        self.sim_damage = []
        
    def __repr__(self):
        return f'Simulation(attacker={self.attacker.name}, target={self.target.name}, weapon={self.weapon.name})'
     
    
    @classmethod
    def from_dataframes(cls, at_frame, tg_frame, wp_frame, n:int = 10000):
        default_attacker = {'hitmod':0, 'woundmod':0, 'unit_type':'infantry', 'no_models':1}
        default_target = {'unit_type':'infantry', 'hitmod':0, 'woundmod':0, 'invun_save':0}
        default_weapon = {'shot_type':'flat', 'shot_mod':0, 'dmg_type':'flat', 'dmg_mod':0}
        attacker = unit_classes.Attacker(*at_frame.fillna(value=default_attacker))
        target = unit_classes.Target(*tg_frame.fillna(value=default_target))
        weapon = unit_classes.Weapon(*wp_frame.fillna(value=default_weapon))
        return cls(attacker, target, weapon, n)
    
    @classmethod
    def from_csv_datafiles(cls, at_file : str, tg_file : str, wp_file : str, n:int = 10000):
        default_attacker = {'hitmod':0, 'woundmod':0, 'unit_type':'infantry', 'no_models':1}
        default_target = {'unit_type':'infantry', 'hitmod':0, 'woundmod':0, 'invun_save':0}
        default_weapon = {'shot_type':'flat', 'shot_mod':0, 'dmg_type':'flat', 'dmg_mod':0}
        
        attacker = unit_classes.Attacker(*pd.read_csv(at_file, skipinitialspace=True).iloc[0].fillna(value=default_attacker))
        target = unit_classes.Target(*pd.read_csv(tg_file, skipinitialspace=True).iloc[0].fillna(value=default_target))
        weapon = unit_classes.Weapon(*pd.read_csv(wp_file, skipinitialspace=True).iloc[0].fillna(value=default_weapon))
        return cls(attacker, target, weapon, n)
        

    @staticmethod
    def __restrict_value(value, min, max)->float:
        '''This funtion restricts dice throws to the interval [min,max]
        
        :param value the current value
        :param min start of the interval
        :param max end of the interval
        '''
        if(value>max):
            return max
        elif(value<min):
            return min
        else:
            return value
        
    @staticmethod
    def gauss(A, x):
        a = A[0]
        mu = A[1]
        sigma = A[2]
        return np.exp(-(x-mu)**2/(2.0*sigma**2))/np.sqrt(2.0*np.pi*sigma**2)*a
    
    @staticmethod
    def gauss_norm(A, x):
        mu = A[0]
        sigma = A[1]
        return np.exp(-(x-mu)**2/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma)
    
    def __num_shots(self,randi)->int:
        if(self.weapon.shot_type=='flat'):
            num_shots = self.weapon.num_shots + self.weapon.shot_mod
        else:
            num_shots = randi.randint(1,self.weapon.num_shots) + self.weapon.shot_mod
        return num_shots
    
    def __hitroll(self, randi)->bool:
        hit_roll = randi.randint(1,6)
        if(hit_roll == 1):
            return False
        hit_mod = self.__restrict_value(self.attacker.hit_mod + self.target.hit_mod, -1, 1)
        hit_roll = self.__restrict_value(hit_roll + hit_mod, 1, 6)
        if(hit_roll < self.attacker.ws ):
            return False
        else:
            return True

    def __woundroll(self, randi)->bool:
        wound_roll = randi.randint(1,6)
        if(wound_roll==1):
            return False
        wound_mod = self.__restrict_value(self.attacker.wound_mod + self.target.wound_mod, -1, 1)
        wound_roll = self.__restrict_value(wound_roll + wound_mod, 1, 6)
        #check wound roll results
        if(self.weapon.strength == self.target.toughness and wound_roll < 4):
            return False
        elif(2*self.weapon.strength <= self.target.toughness and wound_roll < 6):
            return False
        elif(self.weapon.strength < self.target.toughness and wound_roll < 5):
            return False
        elif(self.weapon.strength > self.target.toughness and wound_roll < 3):
            return False
        return True

    def __armorsave(self, randi)->bool:
        random.Random()
        #check if armor can save the attack or invun save exists
        if(self.target.armor - self.weapon.ap < 7 or self.target.invun_save!=0):
            save_roll = randi.randint(1,6)
            if(self.target.armor - self.weapon.ap > self.target.invun_save and self.target.invun_save != 0):
                save = self.target.invun_save
            else:
                save = self.target.armor
                save_roll = self.__restrict_value(save_roll + self.weapon.ap, 1, 6)
            if(save_roll > save):
                return False
            
        return True

    def __weapon_dmg(self, randi)->float:
        dmg = 0
        if(self.weapon.dmg_type == 'flat'):
            dmg = self.weapon.dmg + self.weapon.dmg_mod
        elif(self.weapon.dmg_type == 'random' or self.weapon.dmg_type == 'mixed'):
            dmg = randi.randint(1,self.weapon.dmg) + self.weapon.dmg_mod
        else:
            raise ValueError
        return dmg
    
    def __attack_sequence(self, randi)->float:
        '''This function simulates one attack by the attacker
            against the target using the given weapon
            
            Return
            float damage dealt with this attack
        '''
        dmg = 0
        #check if attack hit target
        if(not self.__hitroll(randi)):
            #print('didnt hit')
            return 0
        #check if attack wounded
        if(not self.__woundroll(randi)):
            #print('didnt wound')
            return 0 
        #check armorsave of target
        if(not self.__armorsave(randi)):
            #print('armor saved')
            return 0
        
        try:
            dmg += self.__weapon_dmg(randi)
        except ValueError:
            print('not supported weapon type used!')
            dmg += -1
        return dmg
        

    def unit_shooting_infantry(self)->float:
        '''This method simulates the attack sequence of one unit against
            a infantry unit target using the given weapon. This method 
            will calcualte the number of slain models.
            
            Return:
            float: number of slain models
        
        '''
        remain_hp = self.target.hp
        models_killed = 0
        randi = random.Random()

        for _ in range(self.attacker.no_models):
            for _ in range(self.__num_shots(randi)):
                dmg = self.__attack_sequence(randi)
                if(dmg >= remain_hp):
                    models_killed += 1
                    remain_hp = self.target.hp
                else:
                    remain_hp -= dmg
        return models_killed + (self.target.hp-remain_hp)/float(self.target.hp)        
        
    def unit_shooting_vehicle(self)->float:
        '''This method simulates the attack sequence of one unit against
            a vehicle unit using the given weapon. This method 
            will calcualte the total damage dealt.
            
            Return:
            float: total damage dealt
        '''
        dmg = 0
        randi = random.Random()
        for _ in range(self.attacker.no_models):
            for _ in range(self.__num_shots(randi)):
                dmg += self.__attack_sequence(randi)
        return dmg
    
    def simulate_attack_sequence(self):
        if(self.target.unit_type == 'infantry'):
            func = self.unit_shooting_infantry
        elif(self.target.unit_type == 'vehicle'):
            func = self.unit_shooting_vehicle
        else:
            raise TypeError('No valid target unit type selected.')
        
        results = np.empty(self.num_runs)
        for i in range(self.num_runs):
            results[i] = func()
        return results
    
    def visualize_data(self, data, normalized:bool=False)->plt.Figure:
        if(self.target.unit_type=='infantry'):
            max_dmg = int(np.max(data)+1)
            bins = np.arange(-1/(2*self.target.hp), max_dmg, 1/float(self.target.hp))
            xlabel = f'Number of {self.target.name} models killed'
        else:
            max_dmg = int(np.max(data)+1)
            bins = np.arange(-0.5, max_dmg)
            xlabel = f'Damage infliceted to {self.target.name}'
        
        if not normalized:
            ylabel = 'Number of events'
        else:
            ylabel = 'Relative probability'
        fig = plt.figure(1,(8,6))
        ax1 = fig.add_subplot(111)    
        ax1.hist(data, bins=bins, density=normalized, label='simulated damage')
        ax1.set_ylabel(ylabel)
        ax1.set_xlabel(xlabel)
        ax1.set_title(f'{self.attacker.name} attacking {self.target.name} with {self.weapon.name}')
        ax1.legend()
        return fig
    
    def analyze_data(self, data, normalized:bool = False):
        max_dmg = int(np.max(data)+1)
        if(self.target.unit_type=='infantry'):
            bins = np.arange(-1/(2*self.target.hp), max_dmg, 1/float(self.target.hp))
        else:
            bins = np.arange(-0.5, max_dmg+0.5)
            
        hist, bins = np.histogram(data, bins=bins, density=normalized)
        dmg_points = [bins[i]-(bins[i]-bins[i-1])/2.0 for i in range(1,len(bins))]
        yerr = np.sqrt(hist)
        if(self.target.unit_type=='infantry'):
            xerr = np.ones(len(dmg_points))*1.0/(np.sqrt(12.0)*self.target.hp)
        else:
            xerr = np.ones(len(dmg_points))*1.0/np.sqrt(12.0)
        
        if normalized:    
            gaussf = odr.Model(self.gauss_norm)
            beta = [1.0, 0.5]
        else:
            gaussf = odr.Model(self.gauss)
            beta = [self.num_runs, 1.0, 0.5]

        yerr = np.array([x if x !=0 else 2.0 for x in yerr])
        
        dataODR = odr.RealData(dmg_points, y=hist, sx=xerr, sy=yerr)
        myodr = odr.ODR(dataODR, gaussf, beta0=beta)
        output = myodr.run()
        params, errors = output.beta, output.sd_beta
        return (params, errors)
    
    def visualize_fit(self, params, fig:plt.Figure, normalized:bool=False)->plt.Figure:
        ax = fig.get_axes()[0]
        x = np.linspace(0.0, int(ax.get_xlim()[1]+1), 100)
        if(normalized):
            y = self.gauss_norm(params, x)
        else:
            y = self.gauss(params, x)
        ax.plot(x,y, ':', label='fit curve')
        ax.legend()
    
def main()->None:
   marine = unit_classes.attacker('marine', 3, 20, no_models=5)
   guardsmen = unit_classes.target('guardsmen', 3, 5, 1)
   rhino = unit_classes.target('rhino', 7, 3, 11, unit_type='vehicle')
   custodes = unit_classes.target('custodes', 5, 2, 3)
   bolt_rifle = unit_classes.weapon('Bolt Rifle', 2, 4, -1, 1)
   
   sim = Simulation(marine, custodes, bolt_rifle)
   max_dmg = (sim.attacker.no_models*sim.weapon.num_shots)/float(sim.target.hp)
   array = np.ones(10000)
   for i in range(10000):
    array[i] = dmg = sim.unit_shooting_infantry()
   plt.hist(array, 12, range=(0,max_dmg))
   plt.show()
           

if __name__ == '__main__':
    main()