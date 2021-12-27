import PySimpleGUI as sg
import src.layouts
import unit_classes
from simulation import Simulation

def create_attacker(values) -> unit_classes.Attacker :
    if values['-ATTACKER-NAME-'] == '' : 
        name = 'attacker'
        print('No attacker name given. Using default name attacker.')
    else : name = values['-ATTACKER-NAME-']
    
    try:
        ws = int(values['-ATTACKER-WS-'])
    except ValueError:
        print('Failed to convert attacker weapon skill')
        return None
    
    try:
        ppm = int(values['-ATTACKER-PPM-'])
    except ValueError:
        print('No points per model given. Points cost of 1 will be assumed.')
        ppm = 1
    
    try:
        num_models = int(values['-ATTACKER-NUMMODELS-'])
    except ValueError:
        print('No number of models given. A single model will be assumed')
        num_models = 1
        
    unit_type = values['-ATTACKER-UNITTYPE-']
    
    return unit_classes.Attacker(name, ws, ppm, unit_type=unit_type, no_models=num_models)    
    
def create_target(values) -> unit_classes.Target :
    if values['-TARGET-NAME-'] == '' : 
        name = 'target'
        print('No target name given. Using default name target.')
    else: name = values['-TARGET-NAME-']
    
    try:
        toughness = int(values['-TARGET-TOUGHNESS-'])
    except ValueError:
        print('Falied to convert toughness. No target created.')
        return None
    
    try:
        armor = int(values['-TARGET-ARMOR-'])
    except ValueError:
        print('Falied to convert target armor. No target created.')
        return None
    
    unit_type = values['-TARGET-UNITTYPE-']
    
    try:
        hp = int(values['-TARGET-HP-'])
    except ValueError:
        print('No health points given.')
        if unit_type == 'infantry':
            hp = 1
            print('Using 1 hp for infantry models')
        elif unit_type == 'vehicle':
            hp = 20
            print('Using 20 hp for vehicle targets')
        else: return None
        
    try:
        invun_save = int(values['-TARGET-INVUNSAVE-'])
    except ValueError:
        invun_save = 0
        print('No invuknerable save given. Target is assumed to have no invulnerable save.')
        
    return unit_classes.Target(name, toughness, armor, hp, unit_type, invun_save)

def create_weapon(values) -> unit_classes.Weapon :
    if values['-WEAPON-NAME-'] == '':
        name = 'weapon'
        print('No weapon name given. Using default name weapon.')
    else: name = values['-WEAPON-NAME-']
    
    try:
        num_shots = int(values['-WEAPON-NUMSHOTS-'])
    except ValueError:
        print('No number of shots given. No weapon created.')
        return None
    
    try:
        strength = int(values['-WEAPON-STRENGTH-'])
    except ValueError:
        print('No weapon strength given. No weapon created.')
        return None
    
    try:
        ap = int(values['-WEAPON-AP-'])
    except ValueError:
        print('No weapon ap given. Using default value of 0 ap.')
        ap = 0
    
    try:
        dmg = int(values['-WEAPON-DMG-'])
    except ValueError:
        print('N0 weapon damage given. No weapon created.')
        return None
    
    shottype = values['-WEAPON-SHOTTYPE-']
    dmgtype = values['-WEAPON-DMGTYPE-']
    
    try:
        shotmod = int(values['-WEAPON-SHOTMOD-'])
    except ValueError:
        print('No modifier for number of shots given. Using default value of 0.')
        shotmod = 0
        
    try:
        dmgmod = int(values['-WEAPON-DMGMOD-'])
    except ValueError:
        print('No modifier for weapon damage given. Using default value of 0.')
        dmgmod = 0
        
    return unit_classes.Weapon(name, num_shots, strength, ap, dmg, shottype, shotmod, dmgtype, dmgmod)

def create_sim(values):
    modifiers = (int(values['-HITMOD-']), int(values['-WOUNDMOD-']), int(values['-DMGMOD-']))
    try:
        simulation = Simulation(create_attacker(values), create_target(values), create_weapon(values), modifiers=modifiers)
    except TypeError:
        print('Simulation could not be created.')
        simulation = None
    print(simulation)

#create main window
window = sg.Window(title='Hello World', layout=src.layouts.layout, margins=(50,50))
#main event loop
while True:
    event, values = window.read()
    if event == '-EXIT-' or event == sg.WIN_CLOSED:
        window.close()
        break
    elif event == '-CREATESIM-':
        create_sim(values)
    elif event =='-RUNSIM-':
        print(values)
        