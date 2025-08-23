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
CONTROL_PANEL_WIDTH = APP_WIDTH * 0.3
PADDING = 10
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
        self.lang_var = StringVar(value="th")
        
        # Load categories from JSON file
        self.categories = []
        if os.path.exists(CATEGORIES):
            with open(CATEGORIES, 'r', encoding='utf-8') as file:
                self.categories = json.load(file)

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

        display_panel_grid_rows_weight = [1, 2, 10]
        display_panel_grid_columns_weight = [1, 1, 1]
        for i, w in enumerate(display_panel_grid_rows_weight):
            display_panel.grid_rowconfigure(i, weight=w)
        for i, w in enumerate(display_panel_grid_columns_weight):
            display_panel.grid_columnconfigure(i, weight=w)
            
        Label(display_panel, text="Budget Tracker", bg="#ff0000",).grid(row=0, column=0, columnspan=2, sticky="w", padx=PADDING)
        lang_button = Button(display_panel, text="en/th", bg="#00ff00", command=self.toggle_language)
        lang_button.grid(row=0, column=2, sticky="e", padx=PADDING)
        
        # Create input and control panel
        control_panel = Frame(self.root, bg=CONTROL_BG_COLOR, width=CONTROL_PANEL_WIDTH, height=APP_HEIGHT)
        control_panel.grid(row=0, column=1, sticky="nsew")
        control_panel.grid_propagate(False)
        
        # Create tabs in control panel tabs
        control_panel_tabs = ttk.Notebook(control_panel)
        control_panel_tabs.pack(fill="both", expand=True)
        
        # Create input panel inside input and control panel
        input_panel = Frame(control_panel_tabs, bg="#00ff00")
        input_panel.pack(fill="both", expand=True)
        control_panel_tabs.add(input_panel, text="Input")
            
        # Add widgets in input panel
        Label(input_panel, text=self.get_label("วันที่", "Date")).pack()
        Entry(input_panel, textvariable=self.date_var).pack()
        Label(input_panel, text="ประเภท").pack()
        
        # Radio button income
        income_radio = ttk.Radiobutton(input_panel, text="รายรับ", variable=self.transaction_type_var, value="income")
        income_radio.pack(anchor="w", padx=5, pady=2)

        # Radio button expense
        expense_radio = ttk.Radiobutton(input_panel, text="Expense", variable=self.transaction_type_var, value="expense")
        expense_radio.pack(anchor="w", padx=5, pady=2)
        
        Label(input_panel, text="หมวดหมู่").pack()
        Entry(input_panel, textvariable=self.category_var).pack()  
               
            
        # Create widgets in filter panel        
        filter_panel = Frame(control_panel_tabs, bg="#ff0000")
        filter_panel.pack(fill="both", expand=True)
        control_panel_tabs.add(filter_panel, text="Filter") 
        
    def toggle_language(self):
        if self.lang_var.get() == "th":
            self.lang_var.set("en")
        else:
            self.lang_var.set("th")
            
    def get_label(self, th_label, en_label):
        return th_label if self.lang_var.get() == "th" else en_label

if __name__ == "__main__":
    root = Tk()
    app = BudgetTracker(root)
    root.mainloop()
