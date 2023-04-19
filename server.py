import socket

host = '192.168.88.126'
port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    print(f'Listening on port: {port}')
    print(f'Ip address: {host}')
    while True:
        client, addr = s.accept()
        print('Connected by', addr)
        data = b''

        name = b''
        while b'\r\n\r\n' not in name:
            name += s.recv(128).decode()

        with open(name, 'wb') as f:
            while True:
                data = client.recv(1)
                if not data:
                    break
                f.write(data)
                print(data)

        print('File received and saved')

        client.close()



