from dataclasses import dataclass
@dataclass(frozen=True)
class Attacker :
    name: str
    ws: int
    ppm : float
    unit_type : str = 'infantry'
    no_models : int = 1

@dataclass(frozen=True)
class Target :
    name: str
    toughness: int
    armor: int
    hp: int
    unit_type : str =  'infantry'
    invun_save: int = 0

@dataclass(frozen=True)
class Weapon :
    name: str
    num_shots: int
    strength: int
    ap : int
    dmg : float
    shot_type: str = 'flat' #possibilities are flat, random or mixed, mixed has to be used in combination with shot_mod
    shot_mod: int = 0
    dmg_type : str = 'flat' #possibilities are flat, random or mixed, mixed has to be used in combination with dmg_mod
    dmg_mod : int = 0
    
@dataclass
class Modifiers:
    hitmod : int
    woundmod : int
    dmgmod : int
        
    def __init__( self, hitmod, woundmod, dmgmod ) :
        if hitmod > 1 :
            hitmod = 1
        elif hitmod < -1:
            hitmod = -1
        self.hitmod = hitmod
        if woundmod > 1 :
            woundmod = 1
        elif woundmod < -1:
            woundmod = -1
        self.woundmod = woundmod
        if dmgmod > 1:
            dmgmod = 1
        elif dmgmod < -1:
            dmgmod = -1
        self.dmgmod = dmgmod