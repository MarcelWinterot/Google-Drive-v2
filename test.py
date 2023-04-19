import tkinter
from tkinter import filedialog

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

file_path = filedialog.askopenfilename()
print('file_path: ', file_path)