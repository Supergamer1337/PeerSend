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
    
    print(filename)
    # Make sure file is something
    if host == '' and port == '':
        window['-STATE-'].update('Must specify host and port!')
    elif not os.path.isfile(filename):
        window['-STATE-'].update('No file selected!')
    else:
        # Get filesize
        filesize = os.path.getsize(filename)

        # Connect to server
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, int(port)))
        print("[+] Connected")

        # Send file info
        s.send(f"{filename}{SEPERATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
                
        window['-STATE-'].update(f'{os.path.basename(filename)} has been transferred.')
        # Close socket
        s.close()