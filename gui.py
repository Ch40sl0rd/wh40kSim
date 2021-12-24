import PySimpleGUI as sg
import src.layouts

#create main window
window = sg.Window(title='Hello World', layout=src.layouts.layout, margins=(50,50))
#main event loop
while True:
    event, values = window.read()
    if event == '-EXIT-' or event == sg.WIN_CLOSED:
        window.close()
        break
    elif event == '-CREATESIM-':
        window['-RESULTSCOL-'].update(visible=True)
    elif event =='-RUNSIM-':
        print(values)
        