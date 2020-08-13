import socket
import tqdm
import os

def server(values, window):
    # Get info from GUI
    SERVER_HOST = values['-HOST-']
    SERVER_PORT = int(values['-PORT-'])
    
    # Network values
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    # Create and use socket
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(1)
    

    # Accept incoming connection
    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    # Recieve client filename and filesize
    recieved = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = recieved.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    # Recieve file
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    window['-STATE-'].update(f'{filename} has been transferred.')

    client_socket.close()

    s.close()