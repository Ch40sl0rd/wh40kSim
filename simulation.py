import numpy as np
import matplotlib.pyplot as plt
import random
import unit_classes

def restrict_value(result, min, max):
    '''
        This funtion restricts dice throws to the interval [min,max]
        
        :param
    '''
    if(result>max):
        return max
    elif(result<min):
        return min
    else:
        return result
    
def attack_sequence(attacker, target, weapon):
    '''
        This function simulates a full attack sequence in wh40k and returns inflicted damage on wehicles or
        target models killed per 100 point for infantry
    '''
    if (isinstance(attacker, unit_classes.attacker)==False):
        raise TypeError
    if(isinstance(target, unit_classes.target)==False):
        raise TypeError
    if(isinstance(weapon, unit_classes.weapon)==False):
        raise TypeError
    
    #hit roll
    random.Random()
    hit_roll = random.randint(1,6)
    hit_mod = restrict_value(attacker.hit_mod + target.hit_mod, -1, 1)
    hit_roll = restrict_value(hit_roll + hit_mod, 1, 6)
    if(hit_roll < attacker.ws or hit_roll == 1):
        return 0
    #wound roll
    wound_roll = random.randint(1,6)
    wound_mod = restrict_value(attacker.wound_mod + target.wound_mod, -1, 1)
    wound_roll = restrict_value(wound_roll + wound_mod, 1, 6)
    #check wound roll results
    if(wound_roll == 1):
        return 0
    elif(weapon.strength == target.toughness and wound_roll < 4):
        return 0
    elif(2*weapon.strength <= target.toughness and wound_roll < 6):
        return 0
    elif(weapon.strength < target.toughness and wound_roll < 5):
        return 0
    elif(weapon.strength >= 2*target.toughness and wound_roll < 2):
        return 0
    elif(weapon.strength > target.toughness and wound_roll < 3):
        return 0
    
    #armorsave
    if(target.armor - weapon.ap < 7):
        save_roll = random.randint(1,6)
        save_roll = restrict_value(save_roll + weapon.ap, 1, 6)
        if(save_roll < target.armor):
            return 0
    
    if(weapon.dmg_type == 'flat'):
        dmg = weapon.dmg + weapon.dmg_mod
    elif(weapon.dmg_type == 'random' or weapon.dmg_type == 'mixed'):
        dmg = random.randint(1,weapon.dmg) + weapon.dmg_mod
    else:
        raise ValueError
    
    return dmg
    

def unit_shooting(attacker, target, weapon):
    if (isinstance(attacker, unit_classes.attacker)==False):
        raise TypeError
    if(isinstance(target, unit_classes.target)==False):
        raise TypeError
    if(isinstance(weapon, unit_classes.weapon)==False):
        raise TypeError
    
    if(target.unit_type == 'infantry'):
        pass
    elif(target.unit_type == 'vehicle'):
        pass
     
def main():
    marine_att = unit_classes.attacker(3, 20)
    marine_tar = unit_classes.target(4, 3, 2)
    bolt_rifle = unit_classes.weapon(2, 8, -4, 6, 'mixed', 2)
    
    for _ in range(10):
        try: 
            dmg = attack_sequence(marine_att, marine_tar, bolt_rifle)
        except TypeError:
            print('Did not use the right classes for attacker, target or weapon')
        except ValueError:
            print('No supported dmg_type used')
        else:
            print(dmg)
    

if __name__ == '__main__':
    main()