import PySimpleGUI as sg
sizeText = (12,1)
sizeInput = (15,1)
tab_attacker =  sg.Tab('Attacker',[
                    [sg.Text('Define the attacker statline')],
                    [sg.Column([
                        [sg.Text('name:', size=sizeText), sg.Input(default_text = 'Intercessor',size=(15,1), key='-ATTACKER-NAME-')],
                        [sg.Text('ws:', size=sizeText), sg.Input(default_text = '3',size = sizeInput, key='-ATTACKER-WS-')],
                        [sg.Text('ppm:', size=sizeText), sg.Input(default_text = '20',size = sizeInput, key='-ATTACKER-PPM-')],
                        [sg.Text('unit type:', size=sizeText), sg.OptionMenu(['infantry','vehicle'],default_value='infantry',size = sizeText, key='-ATTACKER-UNITTYPE-')],
                        [sg.Text('no. models:', size=sizeText ), sg.Input(default_text = '1',size = sizeInput, key='-ATTACKER-NUMMODELS-')]
                     ])]
])

tab_target = sg.Tab('Target', [
                    [sg.Text('Define the target statline')],
                    [sg.Column([
                        [sg.Text('name:', size=sizeText), sg.InputText(default_text = 'Guardsman', size=sizeInput, key='-TARGET-NAME-')],
                        [sg.Text('toughness:', size=sizeText), sg.InputText(default_text = '3', size=sizeInput, key='-TARGET-TOUGHNESS-')],
                        [sg.Text('armor:', size=sizeText), sg.InputText(default_text = '5', size=sizeInput, key='-TARGET-ARMOR-')],
                        [sg.Text('hp:', size=sizeText), sg.InputText(default_text = '1', size=sizeInput, key='-TARGET-HP-')],
                        [sg.Text('unit type:', size=sizeText), sg.OptionMenu(['infantry', 'vehicle'],default_value='infantry', size=sizeText, key='-TARGET-UNITTYPE-')],
                        [sg.Text('invun save:', size=sizeText), sg.InputText(default_text='0', size=sizeInput, key='-TARGET-INVUNSAVE-')]
                    ])]
])

tab_weapon = sg.Tab('Weapon', layout=[
                    [sg.Text('Define weapon statline')],
                    [sg.Column([
                        [sg.Text('name:', size=sizeText), sg.Input(default_text = 'Bolt rifle', size=sizeInput, key='-WEAPON-NAME-')],
                        [sg.Text('no. shots:', size=sizeText), sg.Input(default_text = '2', size=sizeInput, key='-WEAPON-NUMSHOTS-')],
                        [sg.Text('strength:', size=sizeText), sg.Input(default_text = '4', size=sizeInput, key='-WEAPON-STRENGTH-')],
                        [sg.Text('ap:', size=sizeText), sg.Input(default_text = '-1', size=sizeInput, key='-WEAPON-AP-')],
                        [sg.Text('damage:', size=sizeText), sg.Input(default_text = '1', size=sizeInput, key='-WEAPON-DMG-')],
                        [sg.Text('shot type:', size=sizeText), sg.OptionMenu(['flat', 'random', 'blast'],default_value='flat', size=sizeText, key='-WEAPON-SHOTTYPE-')],
                        [sg.Text('shot mod:', size=sizeText), sg.Input(default_text = '0', size=sizeInput, key='-WEAPON-SHOTMOD-')],
                        [sg.Text('damage type:', size=sizeText), sg.OptionMenu(['flat', 'random', 'mixed'],default_value='flat', size=sizeText, key='-WEAPON-DMGTYPE-')],
                        [sg.Text('damage mod:', size=sizeText), sg.Input(default_text = '0', size=sizeInput, key='-WEAPON-DMGMOD-')],
                    ])]
])

tab_modifiers = sg.Tab(title='Modifiers', layout=[
                [sg.Text('Define the modifiers')],
                [sg.Column([
                    [sg.Text('Hitmod', size=sizeText), sg.OptionMenu(['+1', '0', '-1'], default_value='0',size=sizeInput, key='-HITMOD-')],
                    [sg.Text('Woundmod', size= sizeText), sg.OptionMenu(['+1', '0', '-1'], default_value='0',size=sizeInput, key='-WOUNDMOD-')],
                    [sg.Text('Dmgmod', size=sizeText), sg.OptionMenu(['0', '-1'], default_value='0',size = sizeInput, key='-DMGMOD-')]
                    ])
                ]                
])

layout_results = [
                [sg.Text('Results of Simulation', key='-RESULTSHEAD-')],
                [sg.Column([
                    [sg.Text('average damage')],
                    [sg.Text('standard deviation')]]
                , key='-RESULTSTEXT-'),
                 sg.Column([
                     [sg.InputText(key='-RESULTSAVERAGE-')],
                     [sg.InputText(key='-RESULTSSIGMA-')]
                 ], key='-RESULTSDATA-')
                ]
]

layout_buttons = [
                [sg.Button('Create Simulation', key='-CREATESIM-')],
                [sg.Button('Simulate attack sequence', key='-RUNSIM-')],
                [sg.Button('show results', key='-RESULTSSHOW-')],
                [sg.Button('Exit', key='-EXIT-')]
]

layout_mainwindow =    [
                [sg.TabGroup([[tab_attacker, tab_target, tab_weapon, tab_modifiers]]), sg.Frame('Results', [[sg.Canvas(size= (20,10),key='-CANVAS-')]])],
                [sg.HorizontalSeparator()],
                [sg.Column(layout_buttons), sg.VerticalSeparator(), sg.Frame('Log', [[sg.Multiline(size=(65,10), autoscroll=True, write_only=True, reroute_stdout=True)]]) ]
            ]