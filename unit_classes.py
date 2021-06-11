from dataclasses import dataclass
@dataclass(frozen=True)
class attacker :
    name: str
    ws: int
    ppm : float
    hit_mod : int = 0
    wound_mod : int = 0
    unit_type : str = 'infantry'
    no_models : int = 1

@dataclass(frozen=True)
class target :
    name: str
    toughness: int
    armor: int
    hp: int
    unit_type : str =  'infantry'
    hit_mod : int = 0
    wound_mod : int = 0
    invun_save: int = 0

@dataclass(frozen=True)
class weapon :
    name: str
    num_shots: int
    strength: int
    ap : int
    dmg : float
    shot_type: str = 'flat' #possibilities are flat, random or mixed, mixed has to be used in combination with shot_mod
    shot_mod: int = 0
    dmg_type : str = 'flat' #possibilities are flat, random or mixed, mixed has to be used in combination with dmg_mod
    dmg_mod : int = 0
