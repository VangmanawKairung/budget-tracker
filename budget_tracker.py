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
DISPLAY_PANEL_WIDTH = APP_WIDTH * 0.7
CONTROL_PANEL_WIDTH = APP_WIDTH - DISPLAY_PANEL_WIDTH
BG_COLOR = "#212121"  # Background color
FG_COLOR = "#faf9f6"  # Foreground (text) color

# CSV file for persistent storage
CSV_FILE = "transactions.csv"
CATEGORIES = "categories.json"


class BudgetTracker:
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

        self.create_widget()

    def create_widget(self):
        # กำหนด weight ให้ root เพื่อให้แต่ละคอลัมน์ขยายตามขนาดหน้าต่าง
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=7)  # display_panel (70%)
        self.root.grid_columnconfigure(1, weight=3)  # control_panel (30%)

        display_panel = Frame(self.root, bg="#FF0000")
        display_panel.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)

        control_panel = Frame(self.root, bg="#00FF00")
        control_panel.grid(row=0, column=1, sticky="nsew")


if __name__ == "__main__":
    root = Tk()
    app = BudgetTracker(root)
    root.mainloop()
