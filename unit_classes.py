from dataclasses import dataclass
@dataclass
class attacker :
    ws: int
    ppm : float
    hit_mod : int = 0
    wound_mod : int = 0
    unit_type : str = 'infantry'

@dataclass
class target :
    toughness: int
    armor: int
    hp: int
    unit_type = 'infantry'
    hit_mod : int = 0
    wound_mod : int = 0

@dataclass
class weapon :
    num_shots: int
    strength: int
    ap : int
    dmg : float
    dmg_type : str = 'flat' #possibilities are flat, random or mixed, mixed has to be used in combination with dmg_mod
    dmg_mod : int = 0
