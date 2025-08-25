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
APP_WIDTH = 1200
APP_HEIGHT = 800
DISPLAY_PANEL_WIDTH = APP_WIDTH * 0.6
CONTROL_PANEL_WIDTH = APP_WIDTH * 0.4
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
        #################### Window set up ####################
        self.root = root
        self.root.title(APP_TITLE)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (APP_WIDTH // 2)
        y = (screen_height // 2) - (APP_HEIGHT // 2)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        #################### Load categories from JSON file ####################
        self.categories = []
        if os.path.exists(CATEGORIES):
            with open(CATEGORIES, "r", encoding="utf-8") as file:
                loaded_categories = json.load(file)
                self.categories = loaded_categories

        #################### Label variables ####################
        # Display panel labels
        self.title_label = StringVar(value=APP_TITLE)
        self.total_income_label = StringVar(value="0.00")
        self.total_expense_label = StringVar(value="0.00")
        self.total_balance_label = StringVar(value="0.00")
        self.date_label = StringVar(value="วันที่")  # Also used in input panel
        self.type_label = StringVar(
            value="ประเภท"
        )  # Also used in input panel and filter panel
        self.category_label = StringVar(
            value="หมวดหมู่"
        )  # Also used in input panel and filter panel
        self.amount_label = StringVar(value="จำนวนเงิน")  # Also used in input panel
        self.description_label = StringVar(
            value="รายละเอียด"
        )  # Also used in input panel
        self.process_label = StringVar(value="การดำเนินการ")
        self.process_edit_button_label = StringVar(value="แก้ไข")
        self.process_delete_button_label = StringVar(value="ลบ")

        # Input panel labels
        self.add_transaction_label = StringVar(value="เพิ่มรายการ")
        self.category_input_option_label = StringVar(value="เลือกหมวดหมู่")
        self.note_label = StringVar(value="หมายเหตุ (ไม่จำเป็น)")
        self.save_button_label = StringVar(value="บันทึก")
        self.reset_button_label = StringVar(value="ล้างข้อมูล")

        # Filter panel labels
        self.filter_label = StringVar(value="ตัวกรอง")
        self.start_date_filter_label = StringVar(value="วันที่เริ่มต้น")
        self.end_date_filter_label = StringVar(value="วันที่สิ้นสุด")
        self.category_filter_option_label = StringVar(value="ทั้งหมด")
        self.apply_filter_button_label = StringVar(value="ใช้ตัวกรอง")
        self.clear_filter_button_label = StringVar(value="ล้างตัวกรอง")
        self.export_csv_button_label = StringVar(value="ส่งออก CSV")
        self.export_pdf_button_label = StringVar(value="ส่งออก PDF")
        self.delete_all_button_label = StringVar(value="ลบทั้งหมด")

        #################### Common variables ####################
        self.lang_var = StringVar(value="th")
        self.date_var = StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        self.day_var = StringVar(value=datetime.now().day)
        self.month_var = StringVar(value=datetime.now().month)
        self.year_var = StringVar(value=datetime.now().year)
        self.transaction_type_var = StringVar(value="income")
        self.category_var = StringVar()
        self.amount_var = StringVar()
        self.desc_var = StringVar()

        #################### Execute ####################
        self.create_widget()

    # Create main widgets
    def create_widget(self):
        #################### Create display panel ####################
        # Initialize display panel
        display_panel = Frame(
            self.root, bg=DISPLAY_BG_COLOR, width=DISPLAY_PANEL_WIDTH, height=APP_HEIGHT
        )
        display_panel.grid(row=0, column=0, sticky="nsew", pady=PADDING, padx=PADDING)
        display_panel.grid_propagate(False)

        # Configure grid layout for display panel
        display_panel_grid_rows_weight = [1, 2, 10]
        display_panel_grid_columns_weight = [1, 1, 1]
        for i, w in enumerate(display_panel_grid_rows_weight):
            display_panel.grid_rowconfigure(i, weight=w)
        for i, w in enumerate(display_panel_grid_columns_weight):
            display_panel.grid_columnconfigure(i, weight=w)

        # Add title and language toggle button
        Label(
            display_panel,
            textvariable=self.title_label,
            bg="#ff0000",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=PADDING)
        lang_button = Button(
            display_panel, text="EN | TH", bg="#00ff00", command=self.toggle_language
        )
        lang_button.grid(row=0, column=2, sticky="e", padx=PADDING)

        #################### Create control panel ####################
        control_panel = Frame(
            self.root, bg=CONTROL_BG_COLOR, width=CONTROL_PANEL_WIDTH, height=APP_HEIGHT
        )
        control_panel.grid(row=0, column=1, sticky="nsew")
        control_panel.grid_propagate(False)

        # Create control panel tabs
        control_panel_tabs = ttk.Notebook(control_panel)
        control_panel_tabs.pack(fill="both", expand=True)

        # Create input panel inside control panel
        input_panel = Frame(control_panel_tabs, bg="#00ff00")
        input_panel.pack(fill="both", expand=True)
        control_panel_tabs.add(input_panel, text="Input")

        # Add widgets in input panel
        ## Add date input to input panel
        Label(input_panel, textvariable=self.date_label).pack()

        date_input_panel = Frame(input_panel, bg="#0000ff")
        date_input_panel.pack()
        date_input_panel.grid_rowconfigure(0, weight=1)
        for i in range(3):
            date_input_panel.grid_columnconfigure(i, weight=1)

        days = [str(d) for d in range(1, 32)]
        months = [str(m) for m in range(1, 13)]
        years = [str(y) for y in range(2000, datetime.now().year + 1)]

        day_option = ttk.Combobox(
            date_input_panel,
            textvariable=self.day_var,
            values=days,
        ).grid(row=0, column=0)
        month_option = ttk.Combobox(
            date_input_panel,
            textvariable=self.month_var,
            values=months,
        ).grid(row=0, column=1)
        year_option = ttk.Combobox(
            date_input_panel,
            textvariable=self.year_var,
            values=years,
        ).grid(row=0, column=2)

        ## Add radio buttons income and expense to input panel
        Label(input_panel, textvariable=self.type_label).pack()
        self.income_radio = ttk.Radiobutton(
            input_panel,
            text=self.get_label("รายรับ", "Income"),
            variable=self.transaction_type_var,
            value="income",
            command=self.get_category_values,
        )
        self.income_radio.pack()
        self.expense_radio = ttk.Radiobutton(
            input_panel,
            text=self.get_label("รายจ่าย", "Expense"),
            variable=self.transaction_type_var,
            value="expense",
            command=self.get_category_values,
        )
        self.expense_radio.pack()

        ## Add category input to input panel
        Label(input_panel, textvariable=self.category_label).pack()
        self.categorie_option = ttk.Combobox(
            input_panel, textvariable=self.category_var, state="readonly"
        )
        self.get_category_values()
        self.categorie_option.current(0)
        self.categorie_option.pack()

        ## Add amount input to input panel
        Label(input_panel, textvariable=self.amount_label).pack()
        Entry(input_panel, textvariable=self.amount_var).pack()

        # Create widgets in filter panel
        filter_panel = Frame(control_panel_tabs, bg="#ff0000")
        filter_panel.pack(fill="both", expand=True)
        control_panel_tabs.add(filter_panel, text="Filter")

    # Toggle language function
    def toggle_language(self):

        # Toggle between "th" and "en"
        if self.lang_var.get() == "th":
            self.lang_var.set("en")
        else:
            self.lang_var.set("th")

        # Update all labels based on the selected language
        self.total_income_label.set(self.get_label("รายรับทั้งหมด", "Total Income"))
        self.total_expense_label.set(self.get_label("รายจ่ายทั้งหมด", "Total Expense"))
        self.total_balance_label.set(self.get_label("ยอดคงเหลือ", "Total Balance"))
        self.date_label.set(self.get_label("วันที่", "Date"))
        self.type_label.set(self.get_label("ประเภท", "Type"))
        self.category_label.set(self.get_label("หมวดหมู่", "Category"))
        self.amount_label.set(self.get_label("จำนวนเงิน", "Amount"))
        self.description_label.set(self.get_label("รายละเอียด", "Description"))
        self.process_label.set(self.get_label("การดำเนินการ", "Process"))
        self.process_edit_button_label.set(self.get_label("แก้ไข", "Edit"))
        self.process_delete_button_label.set(self.get_label("ลบ", "Delete"))
        self.add_transaction_label.set(self.get_label("เพิ่มรายการ", "Add Transaction"))
        self.category_input_option_label.set(
            self.get_label("เลือกหมวดหมู่", "Select Category")
        )
        self.note_label.set(self.get_label("หมายเหตุ (ไม่จำเป็น)", "Note (Optional)"))
        self.save_button_label.set(self.get_label("บันทึก", "Save"))
        self.reset_button_label.set(self.get_label("ล้างข้อมูล", "Reset"))
        self.filter_label.set(self.get_label("ตัวกรอง", "Filter"))
        self.start_date_filter_label.set(self.get_label("วันที่เริ่มต้น", "Start Date"))
        self.end_date_filter_label.set(self.get_label("วันที่สิ้นสุด", "End Date"))
        self.category_filter_option_label.set(self.get_label("ทั้งหมด", "All"))
        self.apply_filter_button_label.set(self.get_label("ใช้ตัวกรอง", "Apply Filter"))
        self.clear_filter_button_label.set(self.get_label("ล้างตัวกรอง", "Clear Filter"))
        self.export_csv_button_label.set(self.get_label("ส่งออก CSV", "Export CSV"))
        self.export_pdf_button_label.set(self.get_label("ส่งออก PDF", "Export PDF"))
        self.delete_all_button_label.set(self.get_label("ลบทั้งหมด", "Delete All"))

        # Update radiobutton texts
        self.income_radio.config(text=self.get_label("รายรับ", "Income"))
        self.expense_radio.config(text=self.get_label("รายจ่าย", "Expense"))

        # Update category values in combobox
        self.get_category_values()

    # Helper function to get label based on language
    def get_label(self, th_label, en_label):
        return th_label if self.lang_var.get() == "th" else en_label

    # Get category values based on transaction type and language
    def get_category_values(self):
        print(self.transaction_type_var.get())
        if self.transaction_type_var.get() == "income":
            self.categorie_option["values"] = [
                category["th"] if self.lang_var.get() == "th" else category["en"]
                for category in self.categories["income"]
            ]
        else:
            self.categorie_option["values"] = [
                category["th"] if self.lang_var.get() == "th" else category["en"]
                for category in self.categories["expense"]
            ]
        self.categorie_option.current(0)
        print(self.categorie_option["values"])

    # Set the selected date in the date input fields
    def set_selected_date(self):
        self.date_var.set(
            datetime(
                self.year_var.get(), self.month_var.get(), self.day_var.get()
            ).strftime("%d-%m-%Y")
        )

        print(self.date_var.get())


if __name__ == "__main__":
    root = Tk()
    app = BudgetTracker(root)
    root.mainloop()
