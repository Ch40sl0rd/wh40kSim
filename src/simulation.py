import random

from pandas.core.indexes.base import InvalidIndexError
import src.unit_classes as unit_classes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.odr as odr
from dataclasses import dataclass
import yaml
from dataclasses import dataclass, fields, asdict

@dataclass
class Simulation():
    attacker : unit_classes.Attacker
    target : unit_classes.Target
    weapon : unit_classes.Weapon
    modifiers : unit_classes.Modifiers = None
    num_runs : int = 10000
    
    def __init__(self, attacker, target, weapon, modifiers = None, num_runs:int = 10000):
        if not isinstance(attacker, unit_classes.Attacker):
            raise TypeError('selected attacker is not of type attacker')
        if not isinstance(target, unit_classes.Target):
            raise TypeError('selected target is not of type target')
        if not isinstance(weapon, unit_classes.Weapon):
            raise TypeError('selected weapon is not of type weapon')
        if not isinstance(modifiers, unit_classes.Modifiers):
            raise TypeError('selected modifier is not of type modifier')
        if modifiers == None:
            self.modifiers = unit_classes.Modifiers(0,0,0)
        else:
            self.modifiers = modifiers
        self.attacker = attacker
        self.target = target
        self.weapon = weapon
        self.num_runs = num_runs        
        
    def __repr__(self):
        return f'Simulation(attacker={self.attacker.name}, target={self.target.name}, weapon={self.weapon.name}, modifiers={self.modifiers})'
    
    @classmethod
    def from_yaml(cls, yaml_file: str): 
        with open(yaml_file, "r") as f:
            #load data from yaml file
            data = yaml.load(f, Loader=yaml.SafeLoader)
            #get available fields from Simulation class
            class_fields = {f.name for f in fields(cls)}
            #filter only available fields from class and convert all keys to lowercase
            data = {k.lower(): v for k, v in data.items() if k.lower() in class_fields}
            return cls( unit_classes.Attacker.from_dict(data['attacker']),
                        unit_classes.Target.from_dict(data['target']),
                        unit_classes.Weapon.from_dict(data['weapon']),
                        unit_classes.Modifiers.from_dict(data['modifiers']),
                        data['num_runs'])
            
    def save_to_yaml(self, filename):
        with open(filename, "w") as f:
            yaml.dump(asdict(self), f)
        
        

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
    
    def __num_shots(self,randi)->int:
        if(self.weapon.shot_type=='flat'):
            num_shots = self.weapon.num_shots + self.weapon.shot_mod
        else:
            num_shots = randi.randint(1,self.weapon.num_shots+1) + self.weapon.shot_mod
        return num_shots
    
    def __hitroll(self, randi)->bool:
        hit_roll = randi.randint(1,7)
        if(hit_roll == 1):
            return False
        hit_roll = self.__restrict_value(hit_roll + self.modifiers.hitmod, 1, 6)
        if(hit_roll < self.attacker.ws ):
            return False
        else:
            return True

    def __woundroll(self, randi)->bool:
        wound_roll = randi.randint(1,7)
        if(wound_roll==1):
            return False
        wound_roll = self.__restrict_value(wound_roll + self.modifiers.woundmod, 1, 6)
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
        #check if armor can save the attack or invun save exists
        if(self.target.armor - self.weapon.ap < 7 or self.target.invun_save!=0):
            save_roll = randi.randint(1,7)
            if(self.target.armor - self.weapon.ap > self.target.invun_save and self.target.invun_save ):
                save = self.target.invun_save
            else:
                save = self.target.armor
                save_roll = self.__restrict_value(save_roll + self.weapon.ap, 1, 6)
            if(save_roll >= save):
                return False
            
        return True

    def __weapon_dmg(self, randi)->float:
        dmg = 0
        if(self.weapon.dmg_type == 'flat'):
            dmg = self.weapon.dmg + self.weapon.dmg_mod + self.modifiers.dmgmod
            if dmg <= 0 : dmg = 1
        elif(self.weapon.dmg_type == 'random' or self.weapon.dmg_type == 'mixed'):
            dmg = randi.randint(1,self.weapon.dmg+1) + self.weapon.dmg_mod + self.modifiers.dmgmod
            if dmg <= 0 : dmg = 1
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

    def shooting_combined(self)->float:
        #calcualte total number of shots
        if self.weapon.shot_type == 'random':
            num_shots = np.sum(np.random.randint(1, self.weapon.num_shots+1, size=(self.num_runs,self.attacker.no_models)) + self.weapon.shot_mod, axis = 1)
        else:
            num_shots = self.weapon.num_shots + self.weapon.shot_mod

        hitroll = (np.random.randint(1,7, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.modifiers.hitmod).clip(1,6)
        woundroll = (np.random.randint(1,7, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.modifiers.woundmod).clip(1,6)
        armorroll = (np.random.randint(1,7, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.weapon.ap).clip(1,6)

        if self.weapon.dmg_type == 'random':
            damageroll = (np.random.random_integers(1,self.weapon.dmg+1, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.weapon.dmg_mod + self.modifiers.dmgmod)
        else:
            damageroll = np.ones((self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod)))*(self.weapon.dmg + self.weapon.dmg_mod + self.modifiers.dmgmod)

        for i in range(self.num_runs):
            hitroll[i,num_shots[i]:] = 0
            woundroll[i,num_shots[i]:] = 0
            armorroll[i,num_shots[i]:] = 0

        hits = np.logical_and(hitroll >= self.attacker.ws, hitroll > 1)
        #calculate dice throw needed to wound target
        if(self.weapon.strength == self.target.toughness):
            to_wound = 4
        elif(2*self.weapon.strength <= self.target.toughness):
            to_wound = 6
        elif(self.weapon.strength < self.target.toughness):
            to_wound = 5
        elif(self.weapon.strength > self.target.toughness):
            to_wound = 3
        else:
            to_wound = 2

        wounds = woundroll >= to_wound

        if self.target.armor - self.weapon.ap > self.target.invun_save and self.target.invun_save :
            to_save = self.target.invun_save
        else:
            to_save = self.target.armor

        saves = armorroll < to_save

        return np.sum(damageroll*np.logical_and(np.logical_and(hits, wounds), saves), axis=1) 

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
    
    def simulate_attack_sequence(self)->np.ndarray:
        '''This method simulates a full attack sequence with the attacker, target
            and weapon of the simulation.
            If the target is of unit type infantry, this method will calculate
            the number of target models slain.
            If the target is of unit type vehicle, this method will calculate
            the total damage dealt to such a vehicle.
            
            Return:
            numpy.ndarray: array of the damage dealt or infantry models killed 
        '''
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
        
    
def main()->None:
   pass
           
if __name__ == '__main__':
    main()