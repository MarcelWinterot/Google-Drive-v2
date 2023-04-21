import socket
import tkinter
from tkinter import filedialog
import sys
import os
from config import getData

ip = '127.0.0.1'
port = 5000

def hello(s):
    name = input('What is your name? ')
    s.sendall(f'Hello\r\n{name}\r\n\r\n'.encode())
    response = getData(s)
    param = input('Do you want to create an account - 1 or login - 2? ')
    s.sendall(f'{param}\r\n\r\n'.encode())
    email = input('What is your email? ')
    password = input('What is your password? ')
    s.sendall(f'{email}\r\n\r\n'.encode())
    s.sendall(f'{password}\r\n\r\n'.encode())
    response = getData(s)
    return 1 if '1' in response else 0

def chooseFileOrFolder(option):
    root = tkinter.Tk()

    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    if option == '1':
        file_path = filedialog.askopenfilename()
    elif option == '2':
        file_path = filedialog.askdirectory()
    return file_path

def choose(s):
    option = input('Do you want to send a file - 1 or see your files - 2? ')
    s.sendall(f'{option}'.encode())

    if option == '1':
        print('Wybrana opcja to 1')
        
        file_path = chooseFileOrFolder('1')
        file_size = os.path.getsize(file_path)
        nazwa = file_path.split('/')[-1]
        s.sendall(f'{file_size}\r\n\r\n'.encode())
        s.sendall(f'{nazwa}\r\n\r\n'.encode())

        with open(file_path, 'rb') as file:
            s.sendall(bytes(file.read()))

    elif option == '2':
        print('Wybrana opcja to 2')
        folder_path = chooseFileOrFolder('2')

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
