import random
import unit_classes
import numpy as np
import matplotlib.pyplot as plt

class simulation():
    def __init__(self, attacker, target, weapon):
        if (isinstance(attacker, unit_classes.attacker)==False):
            raise TypeError
        if(isinstance(target, unit_classes.target)==False):
            raise TypeError
        if(isinstance(weapon, unit_classes.weapon)==False):
            raise TypeError
        self.attacker = attacker
        self.target = target
        self.weapon = weapon

    def __restrict_value(self, value, min, max):
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
    
    def __hitroll(self, randi):
        hit_roll = randi.randint(1,6)
        hit_mod = self.__restrict_value(self.attacker.hit_mod + self.target.hit_mod, -1, 1)
        hit_roll = self.__restrict_value(hit_roll + hit_mod, 1, 6)
        if(hit_roll == 1 or hit_roll < self.attacker.ws ):
            return False
        else:
            return True

    def __woundroll(self, randi):
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

    def __armorsave(self, randi):
        random.Random()
        #check if armor can save the attack
        if(self.target.armor - self.weapon.ap < 7):
            #print('armor may save')
            save_roll = randi.randint(1,6)
            save_roll = self.__restrict_value(save_roll + self.weapon.ap, 1, 6)
            if(save_roll > self.target.armor):
                return False
        return True

    def __weapon_dmg(self, randi):
        dmg = 0
        if(self.weapon.dmg_type == 'flat'):
            dmg = self.weapon.dmg + self.weapon.dmg_mod
        elif(self.weapon.dmg_type == 'random' or self.weapon.dmg_type == 'mixed'):
            dmg = randi.randint(1,self.weapon.dmg) + self.weapon.dmg_mod
        else:
            raise ValueError
        return dmg
    
    def __attack_sequence(self):
        '''This function simulates one attack by the attacker
            against the target using the given weapon
            
            Return
            float damage dealt with this attack
        '''
        randi = random.Random()
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
        

    def unit_shooting_infantry(self):
        '''This method simulates the attack sequence of one unit against
            a infantry unit target using the given weapon. This method 
            will calcualte the number of slain models.
            
            Return:
            float: number of slain models
        
        '''
        remain_hp = self.target.hp
        models_killed = 0
        for _ in range(self.attacker.no_models*self.weapon.num_shots):
            dmg = self.__attack_sequence()
            if(dmg >= remain_hp):
                models_killed += 1
                remain_hp = self.target.hp
            else:
                remain_hp -= dmg
        return models_killed + (self.target.hp-remain_hp)/float(self.target.hp)        
        
    def unit_shooting_vehicle(self):
        '''This method simulates the attack sequence of one unit against
            a vehicle unit using the given weapon. This method 
            will calcualte the total damage dealt.
            
            Return:
            float: total damage dealt
        '''
        dmg = 0
        for _ in range(self.attacker.no_models):
            dmg += self.__attack_sequence()
        return dmg
     
def main():
   marine = unit_classes.attacker('marine', 3, 20, no_models=5)
   guardsmen = unit_classes.target('guardsmen', 3, 5, 1)
   rhino = unit_classes.target('rhino', 7, 3, 11, unit_type='vehicle')
   custodes = unit_classes.target('custodes', 5, 2, 3)
   bolt_rifle = unit_classes.weapon('Bolt Rifle', 2, 4, -1, 1)
   
   sim = simulation(marine, custodes, bolt_rifle)
   max_dmg = (sim.attacker.no_models*sim.weapon.num_shots)/float(sim.target.hp)
   array = np.ones(10000)
   for i in range(10000):
    array[i] = dmg = sim.unit_shooting_infantry()
   plt.hist(array, 12, range=(0,max_dmg))
   plt.show()
           

if __name__ == '__main__':
    main()