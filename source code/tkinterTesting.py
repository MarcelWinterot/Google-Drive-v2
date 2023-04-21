import customtkinter

root = customtkinter.CTk()
root.title("Google drive v2")
root.geometry("500x500")
root.resizable(False, False)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

def verifyLogin(email, password):
    print(email, password)

def loginWindow(itemList: list = []):
    for item in itemList:
        item.destroy()
    itemList.clear()

    mainLabel = customtkinter.CTkLabel(master=root, text="Google drive v2", font=("Arial", 48))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

    global emailEntry, passwordEntry
    emailEntry = customtkinter.CTkEntry(master=root, width=340, font=("Arial", 20))
    passwordEntry = customtkinter.CTkEntry(master=root, width=340, show="*", font=("Arial", 20))
    itemList.append(emailEntry)
    itemList.append(passwordEntry)
    emailEntry.place(x=80, y=200)
    passwordEntry.place(x=80, y=240)

    global loginButton
    loginButton = customtkinter.CTkButton(master=root, text="Login", font=("Arial", 24), command=lambda: verifyLogin(emailEntry.get(), passwordEntry.get()))
    itemList.append(loginButton)
    loginButton.place(x=165, y=300)

def chooseWindow(itemList: list):
    for item in itemList:
        item.destroy()
    itemList.clear()
    
    mainLabel = customtkinter.CTkLabel(master=root, text="Google drive v2", font=("Arial", 48))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

    global uploadButton, seeButton
    uploadButton = customtkinter.CTkButton(master=root, text="Upload", font=("Arial", 24), command=lambda: uploadWindow(itemList))
    seeButton = customtkinter.CTkButton(master=root, text="See", font=("Arial", 24), command=lambda: seeWindow(itemList))
    itemList.append(uploadButton)
    itemList.append(seeButton)
    uploadButton.place(x=80, y=250)
    seeButton.place(x=300, y=250)

def uploadWindow(itemList: list):
    for item in itemList:
        item.destroy()
    itemList.clear()

    mainLabel = customtkinter.CTkLabel(master=root, text="Upload your files", font=("Arial", 40))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

def seeWindow(itemList: list):
    for item in itemList:
        item.destroy()
    itemList.clear()

    mainLabel = customtkinter.CTkLabel(master=root, text="See your files", font=("Arial", 40))
    itemList.append(mainLabel)
    mainLabel.pack(pady=70)

loginWindow()

root.mainloop()
