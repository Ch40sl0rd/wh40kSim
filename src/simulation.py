import src.unit_classes as unit_classes
import numpy as np
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
        '''
            This method generates a Simulation object from a yaml file.
            
            params.
            - yaml_file: the file where data is located
            
            returns:
            Simulation object with given data
        '''
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

    def shooting_combined(self)->np.ndarray:
        #calcualte total number of shots
        if self.weapon.shot_type == 'random':
            num_shots = np.sum(np.random.randint(1, self.weapon.num_shots+1, size=(self.num_runs,self.attacker.no_models)) + self.weapon.shot_mod, axis = 1)
        else:
            num_shots = np.ones(self.num_runs, dtype=int)*(self.weapon.num_shots + self.weapon.shot_mod)*self.attacker.no_models

        #generate random dice rolls for hit-, wound- and armorrolls between 1 and 6
        hitroll = (np.random.randint(1,7, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.modifiers.hitmod).clip(1,6)
        woundroll = (np.random.randint(1,7, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.modifiers.woundmod).clip(1,6)
        armorroll = (np.random.randint(1,7, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod)))).clip(1,6)

        if self.weapon.dmg_type == 'random':
            damageroll = (np.random.randint(1,self.weapon.dmg+1, size = (self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod))) + self.weapon.dmg_mod + self.modifiers.dmgmod)
        else:
            damageroll = np.ones((self.num_runs,self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod)))*(self.weapon.dmg + self.weapon.dmg_mod + self.modifiers.dmgmod)

        #set all values above the corresponding number of shots to zero to reduce
        for i in range(self.num_runs):
            hitroll[i,num_shots[i]:] = 0
            woundroll[i,num_shots[i]:] = 0
            armorroll[i,num_shots[i]:] = 0
            
        #check if attack actually hit the target
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

        #check if attack wounds the target
        wounds = woundroll >= to_wound

        #calculate armor or invun save
        if self.target.armor - self.weapon.ap > self.target.invun_save and self.target.invun_save :
            failed_saves = armorroll < self.target.invun_save
        else:
            failed_saves = (armorroll+self.weapon.ap) < self.target.armor

        damage = damageroll*np.logical_and(np.logical_and(hits, wounds), failed_saves)
        
        #calculate total damage for vehicles or number of target models killed for infantry
        if self.target.unit_type == "vehicle":
            return np.sum(damage, axis=1)
        else:
            #calculate minimum damage of a single attack
            if self.weapon.dmg_type == "flat":
                min_damage = self.weapon.dmg+self.weapon.dmg_mod+self.modifiers.dmgmod
            else:
                min_damage = self.weapon.dmg_mod+self.modifiers.dmgmod+1
            #check if minimum damage is equal or larger than target hp
            if self.target.hp <= min_damage:
                return np.sum((damage>0).astype(int), axis=1)
            #otherwise calculate number of slain models
            else:
                slain_models=np.zeros(self.num_runs)
                for i in range(self.num_runs):
                    current_hp = self.target.hp
                    num_models_slain = 0
                    for j in range(self.attacker.no_models*(self.weapon.num_shots+self.weapon.shot_mod)):
                        if current_hp - damage[i, j] < 0:
                            current_hp = self.target.hp
                            num_models_slain += 1
                        else:
                            current_hp -= damage[i, j]
                    slain_models[i] = num_models_slain + current_hp/self.target.hp
                return slain_models
        
    
def main()->None:
   sim = Simulation.from_yaml("database/data.yaml")
   print(sim.shooting_combined())
           
if __name__ == '__main__':
    main()