import socket
import os
import tqdm

def client(values, window):
    # Get info from GUI and Path
    host = values['-HOST-']
    port = values['-PORT-']

    # Network values
    SEPERATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096

    # File info
    filename = values['-FILE-']
    
    # Make host, port and file is used
    if host == '' or port == '':
        window['-STATE-'].update('Must specify host and port!')
    elif not os.path.isfile(filename):
        window['-STATE-'].update('No file selected!')
    else:
        # Get filesize
        filesize = os.path.getsize(filename)

        window['-STATE-'].update(f"Connecting to {host}:{port}.")

        try:
            # Connect to server
            s = socket.socket()
            s.connect((host, int(port)))
            window['-STATE-'].update('Connected...')

            # Send file info
            s.send(f"{filename}{SEPERATOR}{filesize}".encode())
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                window['-STATE-'].update(f"Sending sending {os.path.basename(filename)}:{filesize}")
                for _ in progress:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))

            # Done transferring
            s.close()
            window['-STATE-'].update(f'{os.path.basename(filename)} has been transferred. Waiting for next action...')
        except:
            window['-STATE-'].update('Failed to connect to peer.')