import PySimpleGUI as sg
import client
from client import client
import server
from server import server

# Define layout for window
layout = [  [sg.T('Current State:'), sg.T('not started upload/download', size=(80, 1),  key='-STATE-')],
            [sg.T('Host:'), sg.In(key='-HOST-'), sg.T('Port:'), sg.In(key='-PORT-')],
            [sg.T('Choose File')],
            [sg.In(), sg.FileBrowse(key='-FILE-')],
            [sg.B('Client'), sg.B('Server')]   ]

window = sg.Window('PeerSend', layout)

# Event loop for window.
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Client':
        client(values, window)
    if event == 'Server':
        server(values, window)


window.close()