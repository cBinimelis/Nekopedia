import tkinter as tk
from turtle import position
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(title='Nekopedia', themename='neko_pastel')
root.geometry("1200x720")
root.iconbitmap("assets/favicon.ico")
root.resizable(width=False,height=False)
root.position_center()

login = ttk.Frame(root)
login.pack()
img_login = ImageTk.PhotoImage(Image.open('assets/favicon-0.png'))
label = ttk.Label(login, image=img_login)
label.pack()

root.mainloop()