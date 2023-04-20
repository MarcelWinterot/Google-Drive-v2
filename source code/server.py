import socket
import os
import zipfile

host = '127.0.0.1'
port = 5000


def hello(s):
    name = b''
    while b'\r\n\r\n' not in name:
        name += s.recv(1)
    name = name.decode().strip()
    print(name)
    s.sendall(f'Hello\r\n{name}\r\n\r\n'.encode())

def download(folder_name):
    with zipfile.ZipFile(f'{folder_name}.zip', 'w') as zip:
        for file in os.listdir(folder_name):
            zip.write(f'{folder_name}/{file}')

    file_size = os.path.getsize(f'{folder_name}.zip')

    client.sendall(str(file_size).encode())

    with open(f'{folder_name}.zip', 'rb') as f:
        data = f.read()
        client.sendall(data)

    print('File sent')

    client.close()


def add(size):
    data = b''

    name = b''

    while b'\r\n\r\n' not in name:
        name += client.recv(1)
    print(f"File name: {name.decode().strip()}")
    file_size = int(size)

    with open(f'storedFolders/{addr[0]}/{name.decode().strip()}', 'wb') as f:
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
        hello(client)
        with open('source code/users.txt', 'r') as f:
            users = f.readlines()
            if f'{addr[0]}\n' not in users:
                with open('source code/users.txt', 'a') as f:
                    f.write(f'{addr[0]}\n')
                os.mkdir(f'storedFolders/{addr[0]}')

        param = client.recv(1).decode()

        if param == '1':
            size = client.recv(10).decode().strip()
            print(f"File size: {size}")
            add(size)
        elif param == '2':
            download(addr[0])
        else:
            raise Exception('Invalid option')

        print('Connected by', addr)
