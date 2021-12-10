import PySimpleGUI as sg

layout_attacker =  [
                    [sg.Text('Define the attacker statline')],
                    [sg.Text('name:'), sg.InputText(key='-ATTACKER-NAME-')],
                    [sg.Text('ws:'), sg.InputText(key='-ATTACKER-WS-')],
                    [sg.Text('ppm:'), sg.InputText(key='-ATTACKER-PPM-')],
                    [sg.Text('hitmod:'), sg.InputText(key='-ATTACKER-HITMOD-')],
                    [sg.Text('woundmod:'), sg.InputText(key='-ATTACKER-WOUNDMOD-')],
                    [sg.Text('unit type:'), sg.OptionMenu(['infantry','vehicle'], key='-ATTACKER-UNITTYPE-')],
                    [sg.Text('no. models:'), sg.InputText(key='-ATTACKER-NUMMODELS-')],
                ]

layout_target = [
                    [sg.Text('Define the target statline')],
                    [sg.Text('name:'), sg.InputText(key='-TARGET-NAME-')],
                    [sg.Text('toughness:'), sg.InputText(key='-TARGET-TOUGHNESS-')],
                    [sg.Text('armor:'), sg.InputText(key='-TARGET-ARMOR-')],
                    [sg.Text('hp:'), sg.InputText(key='-TARGET-HP-')],
                    [sg.Text('unit type:'), sg.InputText(key='-TARGET-UNITTYPE-')],
                    [sg.Text('hitmod:'), sg.InputText(key='-TARGET-HITMOD-')],
                    [sg.Text('woundmod:'), sg.InputText(key='-TARGET-WOUNDMOD-')],
                    [sg.Text('invulnerable save:'), sg.InputText(key='-TARGET-INVUNSAVE-')],
                ]

layout_weapon = [
                    [sg.Text('Define weapon statline')],
                    [sg.Text('name:'), sg.InputText(key='-WEAPON-NAME-')],
                    [sg.Text('no. shots:'), sg.InputText(key='-WEAPON-NUMSHOTS-')],
                    [sg.Text('strength:'), sg.InputText(key='-WEAPON-STRENGTH-')],
                    [sg.Text('ap:'), sg.InputText(key='-WEAPON-AP-')],
                    [sg.Text('damage:'), sg.InputText(key='-WEAPON-DMG-')],
                    [sg.Text('name:'), sg.InputText(key='-WEAPON-NAME-')],
                    [sg.Text('shot type:'), sg.InputText(key='-WEAPON-SHOTTYPE-')],
                    [sg.Text('shot mod:'), sg.InputText(key='-WEAPON-NAME-')],
                    [sg.Text('damage type:'), sg.InputText(key='-WEAPON-DMGTYPE-')],
                    [sg.Text('damage mod:'), sg.InputText(key='-WEAPON-DMGMOD-')],
                ]

layout =    [
                [sg.Column(layout_attacker), sg.VerticalSeparator(), sg.Column(layout_target),
                    sg.VerticalSeparator(), sg.Column(layout_weapon)],
                [sg.Button('Exit')]
            ]

#create main window
window = sg.Window(title='Hello World', layout=layout, margins=(100,100))

#main event loop
while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    
window.close()