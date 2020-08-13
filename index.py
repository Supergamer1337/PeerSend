import PySimpleGUI as sg
import threading
import client
from client import client
import server
from server import server

# Define layout for window
layout = [  [sg.T('Current State:'), sg.T('not started upload/download', size=(80, 1),  key='-STATE-')],
            [sg.T('Host:'), sg.In(key='-HOST-'), sg.T('Port:'), sg.In(key='-PORT-')],
            [sg.T('Choose File')],
            [sg.In(), sg.FileBrowse(key='-FILE-')],
            [sg.B('Send'), sg.B('Receive')]   ]

window = sg.Window('PeerSend', layout)

# Event loop for window.
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Send':
        print('Sending to new thread.')
        threading.Thread(target=client, args=(values, window), daemon=True).start()
    if event == 'Receive':
        print('Sending to new thread.')
        threading.Thread(target=server, args=(values, window), daemon=True).start()


window.close()