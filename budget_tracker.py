"""
Budget Tracker GUI Application
Author: Kairung Vangmanaw
Date: August 2025
"""

from tkinter import Tk, Frame, Label, Button, Entry, StringVar, messagebox
from tkinter import ttk
from datetime import datetime
import csv, os, json

# Constants for the application
APP_TITLE = "Budget Tracker"
APP_WIDTH = 1000
APP_HEIGHT = 800
BG_COLOR = "#212121"  # Background color
FG_COLOR = "#faf9f6"  # Foreground (text) color

# CSV file for persistent storage
CSV_FILE = "transactions.csv"
CATEGORIES = "categories.json"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (APP_WIDTH // 2)
        y = (screen_height // 2) - (APP_HEIGHT // 2)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

        # Variables
        self.date_var = StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        self.transaction_type_var = StringVar(value="income")
        self.category_var = StringVar()
        self.desc_var = StringVar()
        self.amount_var = StringVar()
        self.balance_var = StringVar(value="0.00")
        self.selectd_page = StringVar(value="Home")

        self.create_main_frame()

    def create_main_frame(self):
        # Navigation Frame
        nav_frame = Frame(self.root, bg=BG_COLOR, width=70, height=APP_HEIGHT)
        nav_frame.pack(side="left", fill="y")

    def show_frame(self, frame_class):
        pass


class Home:
    pass


class Transactions:
    pass


class Report:
    pass


class Setting:
    pass


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
