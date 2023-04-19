import socket
import tkinter
from tkinter import filedialog
import sys
import os

ip = '127.0.0.1'
port = 5000

def hello(s):
    name = input('What is your name? ')
    s.send(f'Hello\r\n{name}\r\n\r\n'.encode())
    response = b''
    while b'\r\n\r\n' not in response:
        response += s.recv(128)

    return 1 if b'Hello\r\n' in response else 0

def chooseFile():
    root = tkinter.Tk()

    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

    file_path = filedialog.askopenfilename()

    return file_path

def choose(s):
    option = input('Do you want to send a file - 1 or see your files - 2? ')
    s.sendall(f'{option}'.encode())

    if option == '1':
        print('Wybrana opcja to 1')
        
        file_path = chooseFile()
        file_size = os.path.getsize(file_path)
        print(file_size)
        nazwa = file_path.split('/')[-1]
        s.sendall(f'{file_size}\r\n\r\n'.encode())
        s.sendall(f'{nazwa}\r\n\r\n'.encode())
        print(nazwa)


        with open(file_path, 'rb') as file:
            s.sendall(bytes(file.read()))

    elif option == '2':
        print('Wybrana opcja to 2')
        # Serwer wysyła plik .zip do clienta i client go odbiera i zapisuje w folderze
        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

        folder_path = filedialog.askdirectory()

        with open(f'{folder_path}/plik.zip', 'wb') as file:
            data = b''
            while True:
                data = s.recv(1)
                if not data:
                    break
                file.write(data)

    else:
        raise Exception('Invalid option')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print('Connected')
        if not hello(s):
            print('Declined by the server')
            sys.exit(1)

        print('Test')


        choose(s)

main()

"""
TODO
1. Dodać tkinter'a


"""

# with open('addr.txt', 'r') as f:
#     users = f.readlines()
#     if ip not in users:
#         with open('addr.txt', 'w') as f:
#             f.write(ip + '