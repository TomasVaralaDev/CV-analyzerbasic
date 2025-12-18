import tkinter as tk
from tkinter import ttk

def apply_dark_theme(style):
    style.theme_use('clam')
    # Tumman teeman taustat ja värit
    style.configure('TFrame', background='#2e2e2e')
    style.configure('TButton', font=('Arial', 12, 'bold'), background='#4a90e2', foreground='#f0f4f7')  # Vaaleat painikkeet
    style.map('TButton', background=[('active', '#357ab8')])
    style.configure('TLabel', background='#2e2e2e', font=('Arial', 12), foreground='#f0f4f7')  # Vaaleat tekstit
    style.configure('TText', background='#3a3a3a', foreground='#f0f4f7', font=('Arial', 11))  # Tumma tausta ja vaalea teksti
    style.configure('TScrollbar', background='#5a5a5a', troughcolor='#3a3a3a', sliderlength=20)  # Vaaleampi scrollbar

def apply_light_theme(style):
    style.theme_use('clam')
    # Vaalean teeman pehmeät värit
    style.configure('TFrame', background='#f5f5f5')  # Vaaleampi tausta
    style.configure('TButton', font=('Arial', 12, 'normal'), background='#4a90e2', foreground='#ffffff')  # Kirkas tausta
    style.map('TButton', background=[('active', '#357ab8')])
    style.configure('TLabel', background='#f5f5f5', font=('Arial', 12, 'normal'), foreground='#333333')  # Tummat tekstit
    style.configure('TText', background='#ffffff', foreground='#333333', font=('Arial', 11))  # Vaalea tausta ja tummat tekstit
    style.configure('TScrollbar', background='#e1e1e1', troughcolor='#f5f5f5', sliderlength=20)  # Pehmeä scrollbar
