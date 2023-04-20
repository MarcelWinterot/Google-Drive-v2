import socket
import os
import zipfile
from config import getData

host = '127.0.0.1'
port = 5000

"""
from Crypto.Cipher import AES
import binascii

key = 'e08af43a03090ab2c9df32e85a494261'

def encryptPassword(key, message):
    cipher = AES.new(binascii.unhexlify(key), AES.MODE_ECB)
    padded_message = message + (AES.block_size - len(message) % AES.block_size) * chr(AES.block_size - len(message) % AES.block_size)
    ciphertext = cipher.encrypt(padded_message.encode('utf-8'))
    return ciphertext

zrobilem to ale wyskakuje zbyt duzo bledow, naprawie kiedys
"""


def confirmLogin(mail, password):
    with open('source code/users.txt', 'r') as f:
        usersAndPasswords = f.readlines()
    for user in usersAndPasswords:
        user = user.split()
        if mail == user[0]:
            if password == user[1]:
                print("y")
                return 1, mail
            else:
                return 0, mail
    return 0, mail

def createAccount(mail, password):
    with open('source code/users.txt', 'r') as f:
        usersAndPasswords = f.readlines()
    if mail in usersAndPasswords:
        isAlreadyIn = True
    else:
        isAlreadyIn = False

    if not isAlreadyIn:
        with open('source code/users.txt', 'a') as f:
            f.write(f'{mail} {password}\n')
        os.mkdir(f'storedFolders/{mail}')
        return 1, mail
    else:
        return 0, mail

def hello(s):
    name = getData(s)
    print(name)
    s.sendall(f'Hello\r\n{name}\r\n\r\n'.encode())
    param = getData(s)
    mail = getData(s)
    password = getData(s)
    if param == '1':
        return createAccount(mail, password)
    elif param == '2':
        return confirmLogin(mail, password)
    else:
        s.close()
        return 0, mail


def download(folder_name):
    folder_name = f'storedFolders/{folder_name}'
    with zipfile.ZipFile(f'{folder_name}.zip', 'w') as zip:
        for file in os.listdir(folder_name):
            zip.write(f'{folder_name}/{file}')

    with open(f'{folder_name}.zip', 'rb') as f:
        data = f.read()
        client.sendall(data)

    print('File sent')

    client.close()


def add(size, folder_name):
    folder_name = f'storedFolders/{folder_name}'
    name = getData(client)

    print(f"File name: {name}")
    file_size = int(size)

    with open(f'{folder_name}/{name}', 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            data = client.recv(min(file_size - bytes_received, 1024))
            if not data:
                break
            f.write(data)
            bytes_received += len(data)

    print('File received and saved')

    client.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((host, port))
    s.listen(1)
    print(f'Listening on port: {port}')
    print(f'Ip address: {host}')

    while True:
        client, addr = s.accept()
        print('Connected by', addr)
        case, mail = hello(client)
        if case == 1:
            client.sendall('1\r\n\r\n'.encode())
        else:
            client.sendall('0\r\n\r\n'.encode())
            client.close()
            continue

        param = client.recv(1).decode() #Użyliśmy tu recv bez pętli, ponieważ wysyłamy tylko jeden bajt

        if param == '1':
            size = getData(client)
            print(f"File size: {size}")
            add(size, mail)
        elif param == '2':
            download(mail)
        else:
            raise Exception('Invalid option')