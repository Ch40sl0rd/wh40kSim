import PySimpleGUI as sg

layout_attacker =  [
                    [sg.Text('Define the attacker statline')],
                    [sg.Column([
                        [sg.Text('name:')],
                        [sg.Text('ws:')],
                        [sg.Text('ppm:')],
                        [sg.Text('unit type:')],
                        [sg.Text('no. models:')]], size=(80,250) ),
                    sg.Column([
                        [sg.InputText(key='-ATTACKER-NAME-')],
                        [sg.InputText(key='-ATTACKER-WS-')],
                        [sg.InputText(key='-ATTACKER-PPM-')],
                        [sg.OptionMenu(['infantry','vehicle'],default_value='infantry', key='-ATTACKER-UNITTYPE-')],
                        [sg.InputText(key='-ATTACKER-NUMMODELS-')]], size=(100, 250))
                    ]
]

layout_target = [
                    [sg.Text('Define the target statline')],
                    [sg.Column([
                        [sg.Text('name:')],
                        [sg.Text('toughness:')],
                        [sg.Text('armor:')],
                        [sg.Text('hp:')],
                        [sg.Text('unit type:')],
                        [sg.Text('invun save:')]
                    ], size=(80, 250)),
                    sg.Column([
                        [sg.InputText(key='-TARGET-NAME-')],
                        [sg.InputText(key='-TARGET-TOUGHNESS-')],
                        [sg.InputText(key='-TARGET-ARMOR-')],
                        [sg.InputText(key='-TARGET-HP-')],
                        [sg.OptionMenu(['infantry', 'vehicle'],default_value='infantry', key='-TARGET-UNITTYPE-')],
                        [sg.InputText(default_text='0', key='-TARGET-INVUNSAVE-')],
                    ], size=(100, 250))]
                ]

layout_weapon = [
                    [sg.Text('Define weapon statline')],
                    [sg.Column([
                        [sg.Text('name:')],
                        [sg.Text('no. shots:')],
                        [sg.Text('strength:')],
                        [sg.Text('ap:')],
                        [sg.Text('damage:')],
                        [sg.Text('shot type:')],
                        [sg.Text('shot mod:')],
                        [sg.Text('damage type:')],
                        [sg.Text('damage mod:')],
                    ], size=(100, 250)),
                    sg.Column([
                        [sg.InputText(key='-WEAPON-NAME-')],
                        [sg.InputText(key='-WEAPON-NUMSHOTS-')],
                        [sg.InputText(key='-WEAPON-STRENGTH-')],
                        [sg.InputText(key='-WEAPON-AP-')],
                        [sg.InputText(key='-WEAPON-DMG-')],
                        [sg.OptionMenu(['flat', 'random', 'blast'], key='-WEAPON-SHOTTYPE-')],
                        [sg.InputText(key='-WEAPON-SHOTMOD-')],
                        [sg.OptionMenu(['flat', 'random', 'mixed'],key='-WEAPON-DMGTYPE-')],
                        [sg.InputText(key='-WEAPON-DMGMOD-')],
                    ], size=(100, 250))
                    ]
]

layout_modifiers = [
                [sg.Text('Define the modifiers')],
                [sg.Column([
                    [sg.Text('Hitmod')],
                    [sg.Text('Woundmod')],
                    [sg.Text('Dmgmod')]
                    ], size= (80, 150)),
                 sg.Column([
                    [sg.OptionMenu(['+1', '0', '-1'], default_value='0', key='-HITMOD-')],
                    [sg.OptionMenu(['+1', '0', '-1'], default_value='0', key='-WOUNDMOD-')],
                    [sg.OptionMenu(['0', '-1'], default_value='0', key='-DMGMOD-')],
                 ], size=(100, 150))
                ]                
]

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

layout =    [
                [sg.Column(layout_attacker), sg.VerticalSeparator(), sg.Column(layout_target),
                    sg.VerticalSeparator(), sg.Column(layout_weapon), sg.VerticalSeparator(), sg.Column(layout_modifiers)],
                [sg.HorizontalSeparator()],
                [sg.Column(layout_buttons), sg.VerticalSeparator(), sg.Column(layout_results, key='-RESULTSCOL-', visible=False)]
            ]