import socket
import tkinter
from tkinter import filedialog

ip = '192.168.88.126'
port = 5000

def hello(socket):
    name = input('What is your name? ')
    socket.send(f'Hello\r\n{name}\r\n\r\n'.encode())
    response = b''
    while b'\r\n\r\n' not in response:
        response += socket.recv(128).decode()

    return 1 if 'Hello\r\n' in response else 0

def choose(socket):
    option = input('Do you want to send a file - 1 or see your files - 2? ')
    #socket.send(f'{option}\r\n\r\n'.encode())
    if option == '1':
        print('Wybrana opcja to 1')

        file_path = filedialog.askopenfilename()

        with open(file_path, 'rb') as file:
            socket.send(file.read())

    elif option == '2':
        pass

    else:
        raise Exception('Invalid option')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print('Connected')

        s.send('test.txt\r\n\r\n'.encode())

        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

        file_path = filedialog.askopenfilename()

        with open(file_path, 'rb') as file:
            s.send(bytes(file.read()))

main()