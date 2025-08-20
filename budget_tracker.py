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
INPUT_CONTROL_PANEL_WIDTH = APP_WIDTH * 0.3
PADDING = 20
BG_COLOR = "#ff0000"  # Background color
FG_COLOR = "#faf9f6"  # Foreground (text) color
CONTROL_BG_COLOR = "#121212"  # Control panel background color
DISPLAY_BG_COLOR = "#171717"  # Display panel background color

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
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

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
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Create display panel
        display_panel = Frame(self.root, bg=DISPLAY_BG_COLOR, width=DISPLAY_PANEL_WIDTH, height=APP_HEIGHT)
        display_panel.grid(row=0, column=0, sticky="nsew", pady=PADDING, padx=PADDING)
        display_panel.grid_propagate(False)

        # Create input and control panel
        input_control_panel = Frame(self.root, bg=CONTROL_BG_COLOR, width=INPUT_CONTROL_PANEL_WIDTH, height=APP_HEIGHT)
        input_control_panel.grid(row=0, column=1, sticky="nsew")
        input_control_panel.grid_propagate(False)
        
        # Configure grid for control panel
        for i in range(2):
            input_control_panel.grid_rowconfigure(i, weight=1)
        for i in range(1):
            input_control_panel.grid_columnconfigure(i, weight=1)
        
        # Create input panel inside input and control panel
        input_panel = Frame(input_control_panel, bg="#00ff00")
        input_panel.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky="ew")
        
        for i in range(10):
            input_panel.grid_rowconfigure(i, weight=1)
        for i in range(2):
            input_panel.grid_columnconfigure(i, weight=1)
            
        # Create widgets in control panel
        Label(input_panel, text="Budget Tracker", bg=CONTROL_BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, columnspan=2, padx=PADDING)
        Label(input_panel, text="Date:", bg=CONTROL_BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w")
        Entry(input_panel, textvariable=self.date_var, bg=FG_COLOR, fg=CONTROL_BG_COLOR).grid(row=1, column=1, padx=(0, PADDING), pady=PADDING, sticky="ew")
        Label(input_panel, text="Program:", bg=CONTROL_BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="w")
        Entry(input_panel, textvariable=self.transaction_type_var, bg=FG_COLOR, fg=CONTROL_BG_COLOR).grid(row=2, column=1, padx=(0, PADDING), pady=PADDING, sticky="ew")
        
        
        # Crete control panel inside input panel
        control_panel = Frame(input_control_panel, bg="#0000ff")
        control_panel.grid(row=1, column=0, padx=PADDING, pady=PADDING)
        
        Label(control_panel, text="Category:", bg=CONTROL_BG_COLOR, fg=FG_COLOR).pack()
        Label(control_panel, text="Category:", bg=CONTROL_BG_COLOR, fg=FG_COLOR).pack()
        Label(control_panel, text="Category:", bg=CONTROL_BG_COLOR, fg=FG_COLOR).pack()
        Label(control_panel, text="Category:", bg=CONTROL_BG_COLOR, fg=FG_COLOR).pack()
        Entry(control_panel, textvariable=self.category_var, bg=FG_COLOR, fg=CONTROL_BG_COLOR).pack(padx=(0, PADDING), pady=PADDING, fill="x")
        

        
        


if __name__ == "__main__":
    root = Tk()
    app = BudgetTracker(root)
    root.mainloop()
