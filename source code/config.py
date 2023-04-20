def getData(s):
    data = b''
    while b'\r\n\r\n' not in data:
        data += s.recv(1)
    return data.decode().strip()
