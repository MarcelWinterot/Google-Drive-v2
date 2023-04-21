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