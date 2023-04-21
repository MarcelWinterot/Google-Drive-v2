# Google Drive v2
## Division of roles
### Marcel - Client
### Tomek - Server

# Table of consents:
1. [Introduction](#introduction)
2. [Usage](#usage)
3. [Code](#code)
4. [Policy](#policy)

## Introduction

### Project is built using socket library, customtkinter library and some other helpful libraries
### Project is heavily inspired by google drive(more on that in Policy section)

## Usage

### When you start the client file you have to type your name and then select if you want to log in or register
![image](https://user-images.githubusercontent.com/113690851/233736659-7ca72633-b99c-40fb-afea-67bcca9ade92.png)
### After that a window will pop up and you will have to type your username and password, which will check if data is correct
![image](https://user-images.githubusercontent.com/113690851/233736894-0fa2292e-485d-4363-b77f-7ff8e28bff36.png)
### After that you have to choose if you want to upload a file or download all your files
![image](https://user-images.githubusercontent.com/113690851/233737085-6ff8690b-9c8d-4fa0-bb82-243cec99825d.png)
### If you choose to upload a file you will have to choose a file from your computer and if you choose to download all your files you will have to choose a folder where you want to download all your files into
## Code

### Client:
```python
import socket
import customtkinter
import sys
import os
from config import getData

ip = '127.0.0.1'
port = 5000

root = customtkinter.CTk()
root.title("Google drive v2")
root.geometry("500x500")
root.resizable(False, False)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


def loginWindow(itemList: list = []):
    root.title("Google drive v2 - Login")
    mainLabel = customtkinter.CTkLabel(master=root, text="Google drive v2", font=("Arial", 48))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

    subLabel1 = customtkinter.CTkLabel(master=root, text="Mail:", font=("Arial", 16))
    subLabel2 = customtkinter.CTkLabel(master=root, text="Password:", font=("Arial", 16))
    itemList.append(subLabel1); itemList.append(subLabel2)
    subLabel1.place(x=75, y=180)
    subLabel2.place(x=75, y=260)

    mailEntry = customtkinter.CTkEntry(master=root, font=("Arial", 24), width=350)
    passwordEntry = customtkinter.CTkEntry(master=root, font=("Arial", 24), show="*", width=350)
    itemList.append(mailEntry); itemList.append(passwordEntry)
    mailEntry.place(x=75, y=210)
    passwordEntry.place(x=75, y=290)

    loginButton = customtkinter.CTkButton(master=root, text="Login", font=("Arial", 24), command=lambda: root.quit())
    itemList.append(loginButton)
    loginButton.place(relx=0.5, rely=0.75, anchor="center")

    root.mainloop()
    m = mailEntry.get()
    p = passwordEntry.get()
    for item in itemList:
        item.destroy()
    return m, p

def registerWindow(itemList: list = []):
    root.title("Google drive v2 - Register")
    mainLabel = customtkinter.CTkLabel(master=root, text="Google drive v2", font=("Arial", 48))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

    subLabel1 = customtkinter.CTkLabel(master=root, text="Mail:", font=("Arial", 16))
    subLabel2 = customtkinter.CTkLabel(master=root, text="Password:", font=("Arial", 16))
    itemList.append(subLabel1); itemList.append(subLabel2)
    subLabel1.place(x=75, y=180)
    subLabel2.place(x=75, y=260)

    mailEntry = customtkinter.CTkEntry(master=root, font=("Arial", 24), width=350)
    passwordEntry = customtkinter.CTkEntry(master=root, font=("Arial", 24), show="*", width=350)
    itemList.append(mailEntry); itemList.append(passwordEntry)

    mailEntry.place(x=75, y=210)
    passwordEntry.place(x=75, y=290)

    registerButton = customtkinter.CTkButton(master=root, text="Register", font=("Arial", 24), command=lambda: root.quit())
    itemList.append(registerButton)
    registerButton.place(relx=0.5, rely=0.75, anchor="center")

    root.mainloop()
    m = mailEntry.get()
    p = passwordEntry.get()
    for item in itemList:
        item.destroy()
    return m, p

def chooseWindow(s, itemList: list = []):
    returnVal = None
    
    def returnValue(value: int):
        nonlocal returnVal
        returnVal = value
        s.sendall(value.encode())
        root.quit()

    for item in itemList:
        item.destroy()
    itemList.clear()
    
    mainLabel = customtkinter.CTkLabel(master=root, text="Google drive v2", font=("Arial", 48))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

    uploadButton = customtkinter.CTkButton(master=root, text="Upload", font=("Arial", 24), command=lambda: returnValue('1'))
    seeButton = customtkinter.CTkButton(master=root, text="See", font=("Arial", 24), command=lambda: returnValue('2'))
    itemList.append(uploadButton)
    itemList.append(seeButton)
    uploadButton.place(x=80, y=250)
    seeButton.place(x=300, y=250)

    root.mainloop()
    for item in itemList:
        item.destroy()
    return returnVal

def uploadWindow():
    returnVal = None
    def returnValue():
        nonlocal returnVal
        customtkinter.CTk().withdraw() # prevents an empty tkinter window from appearing
        filePath = customtkinter.filedialog.askopenfilename() #Files
        returnVal = filePath
        root.quit()

    customtkinter.CTkLabel(master=root, text="Upload your files", font=("Arial", 40)).pack(pady=70)

    customtkinter.CTkButton(master=root, text="Browse your files", font=("Arial", 28), command=lambda: returnValue()).pack(pady=70)

    root.mainloop()
    return returnVal

def seeWindow():
    returnVal = None
    def returnValue():
        nonlocal returnVal
        customtkinter.CTk().withdraw() # prevents an empty tkinter window from appearing
        filePath = customtkinter.filedialog.askdirectory() #Folder
        returnVal = filePath
        root.quit()

    customtkinter.CTkLabel(master=root, text="See your files", font=("Arial", 40)).pack(pady=70)

    customtkinter.CTkButton(master=root, text="Choose a folder, where you want to save your files", font=("Arial", 20), command=lambda: returnValue()).pack(pady=70)

    root.mainloop()
    return returnVal

def hello(s):
    name = input('What is your name? ')
    param = input('Do you want to create an account - 1 or login - 2? ')
    if param == '1':
        email, password = registerWindow()
    elif param == '2':
        email, password = loginWindow()
    else:
        raise Exception('Wrong param')

    s.sendall(f'Hello\r\n{name}\r\n\r\n'.encode())
    response = getData(s)
    s.sendall(f'{param}\r\n\r\n'.encode())
    s.sendall(f'{email}\r\n\r\n'.encode())
    s.sendall(f'{password}\r\n\r\n'.encode())
    response = getData(s)
    return 1 if '1' in response else 0

def choose(s):
    option = chooseWindow(s)

    if option == '1':    
        file_path = uploadWindow()
        file_size = os.path.getsize(file_path)
        nazwa = file_path.split('/')[-1]
        s.sendall(f'{file_size}\r\n\r\n'.encode())
        s.sendall(f'{nazwa}\r\n\r\n'.encode())

        with open(file_path, 'rb') as file:
            s.sendall(bytes(file.read()))

        print('All done! Thank you for your cooperation!')

    elif option == '2':
        folder_path = seeWindow()

        with open(f'{folder_path}/wszystkiePliki.zip', 'wb') as file:
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

        choose(s)

main()
```

### Server:
```python
import socket
import os
import zipfile
from config import getData
import base64

host = '127.0.0.1'
port = 5000


def encryptPassword(password):
    return base64.b64encode(password.encode()).decode()

def confirmLogin(mail, password):
    with open('source code/users.txt', 'r') as f:
        usersAndPasswords = f.readlines()
    for user in usersAndPasswords:
        user = user.split()
        if mail == user[0]:
            userPassword = user[1]
            if encryptPassword(password) == userPassword:
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
            f.write(f'{mail} {encryptPassword(password)}\n')
        os.mkdir(f'storedFolders/{mail}')
        return 1, mail
    else:
        return 0, mail

def hello(s):
    name = getData(s)
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
        for file in os.listdir(f'{folder_name}'):
            zip.write(f'{folder_name}/{file}')

    with open(f'{folder_name}.zip', 'rb') as f:
        data = f.read()
        client.sendall(data)

    os.remove(f'{folder_name}.zip')
    
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
```

### Config:
```python
def getData(s):
    data = b''
    while b'\r\n\r\n' not in data:
        data += s.recv(1)
    return data.decode().strip()
```

## Explenation of the code:
### Client:
#### 1. Gets information from the user, like his name, mail and password, which it sends to the server
#### 2. Gets information about which option did the user choose(upload or download files) and sends it to the server
#### 3a. If user selected upload, user selects a file from his pc, and client converts it to bytes and sends them to the server. 
#### 3b. If users selected download, users selectes a folder, to which the .zip fill will be downladed. Then recieves the file from the server, and saves it there

### Server:
#### 1. Gets mail and password from the client, and checks if it is correct, after which it gets information about selected option
#### 2a. If user selected upload, server gets the file size and file name and saves it like that,
#### 2b. If user selected download, server add the whole folder into a .zip file and sends it to the client

### Config:
#### 1. Just a shortened version of getting information from server or client

## Policy

### 1. We don't own any right to the original Google Drive™, made by Google™
### 2. This project is stricly for educational use, we don't plan on gaining any sort of gains from this
### 3. Fell free to use this code as you wish
