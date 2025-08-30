"""
Budget Tracker GUI Application
Author: Kairung Vangmanaw
Date: August 2025
"""

from tkinter import Tk, Frame, Label, Button, Entry, StringVar, messagebox, Text
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

# Color
TEXT_COLOR = "#f1f0ee"
DISPLAY_BG_COLOR = "#2b2b2b"
CONTROL_BG_COLOR = "#0f0f0f"
INCOME_COLOR = "#95e913"
EXPENSE_COLOR = "#f50c20"
BALANCE_COLOR = "#6262ff"
NORMAL_BTN_COLOR = "#2b2b2b"
NORMAL_BTN_HOVER_COLOR = "#424242"
SUBMIT_BTN_COLOR = "#0404e1"
SUBMIT_BTN_HOVER_COLOR = "#2929ff"
DELETE_BTN_COLOR = "#ff3b4b"
DELETE_BTN_HOVER_COLOR = "#dc0012"

# File
CSV_FILE = "transactions.csv"
CATEGORIES = "categories.json"


class BudgetTracker:
    #################### Initiation ####################
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
        self.root.configure(bg=DISPLAY_BG_COLOR)
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
        ## Heading panel
        self.title_label = StringVar(value=APP_TITLE)
        self.lang_label = StringVar(value="English")

        ## Summary panel
        self.total_income_label = StringVar(value="รายรับทั้งหมด")
        self.total_expense_label = StringVar(value="รายจ่ายทั้งหมด")
        self.total_balance_label = StringVar(value="ยอดคงเหลือ")

        ## Transaction list panel
        self.heading_date_label = StringVar(value="วันที่")
        self.heading_category_label = StringVar(value="หมวดหมู่")
        self.heading_type_label = StringVar(value="ประเภท")
        self.heading_amount_label = StringVar(value="จำนวน")
        self.heading_note_label = StringVar(value="หมายเหตุ")
        self.process_label = StringVar(value="การดำเนินการ")
        self.process_edit_button_label = StringVar(value="แก้ไข")
        self.process_delete_button_label = StringVar(value="ลบ")

        # Input panel labels
        self.add_transaction_label = StringVar(value="เพิ่มรายการ")
        self.date_label = StringVar(value="วันที่")
        self.type_label = StringVar(value="ประเภท")
        self.category_label = StringVar(value="หมวดหมู่")
        self.amount_label = StringVar(value="จำนวนเงิน")
        self.category_input_option_label = StringVar(value="เลือกหมวดหมู่")
        self.note_label = StringVar(value="หมายเหตุ (ไม่จำเป็น)")
        self.save_button_label = StringVar(value="บันทึก")
        self.reset_button_label = StringVar(value="ล้างข้อมูล")

        # Filter panel labels
        # self.filter_label = StringVar(value="ตัวกรอง")
        # self.start_date_filter_label = StringVar(value="วันที่เริ่มต้น")
        # self.end_date_filter_label = StringVar(value="วันที่สิ้นสุด")
        # self.category_filter_option_label = StringVar(value="ทั้งหมด")
        # self.apply_filter_button_label = StringVar(value="ใช้ตัวกรอง")
        # self.clear_filter_button_label = StringVar(value="ล้างตัวกรอง")
        # self.export_csv_button_label = StringVar(value="ส่งออก CSV")
        # self.export_pdf_button_label = StringVar(value="ส่งออก PDF")
        # self.delete_all_button_label = StringVar(value="ลบทั้งหมด")

        #################### Common variables ####################
        # Language toggle variable
        self.lang_var = StringVar(value="th")

        # Total value variables
        self.total_income_var = StringVar(value="0.00")
        self.total_expense_var = StringVar(value="0.00")
        self.total_balance_var = StringVar(value="0.00")

        # Input variables
        self.day_var = StringVar(value=datetime.now().day)
        self.month_var = StringVar(value=datetime.now().month)
        self.year_var = StringVar(value=datetime.now().year)
        self.transaction_type_var = StringVar(value="income")
        self.category_var = StringVar()
        self.amount_var = StringVar()

        # Loaded transaction variable
        self.loaded_transactions = []

        #################### Execute ####################
        self.create_widget()

        # Load existing transactions from CSV file
        if os.path.exists(CSV_FILE):
            self.load_transactions()

        #################### Style Configuration ####################
        style = ttk.Style()
        style.theme_use("default")

        # Normal Button
        style.configure(
            "Normal.TButton",
            background=NORMAL_BTN_COLOR,
            foreground=TEXT_COLOR,
            borderwidth=0,
            focusthickness=3,
            focuscolor="none",
        )
        style.map(
            "Normal.TButton",
            background=[("active", NORMAL_BTN_HOVER_COLOR)],
            foreground=[("disabled", TEXT_COLOR)],
        )

        # Submit Button
        style.configure(
            "Submit.TButton",
            background=SUBMIT_BTN_COLOR,
            foreground=TEXT_COLOR,
            borderwidth=0,
            focusthickness=3,
            focuscolor="none",
        )
        style.map(
            "Submit.TButton",
            background=[("active", SUBMIT_BTN_HOVER_COLOR)],
            foreground=[("disabled", TEXT_COLOR)],
        )

        # Delete Button
        style.configure(
            "Delete.TButton",
            background=DELETE_BTN_COLOR,
            foreground=TEXT_COLOR,
            borderwidth=0,
            focusthickness=3,
            focuscolor="none",
        )
        style.map(
            "Delete.TButton",
            background=[("active", DELETE_BTN_HOVER_COLOR)],
            foreground=[("disabled", TEXT_COLOR)],
        )

        # Lang Button
        style.configure(
            "Lang.TButton",
            background=DISPLAY_BG_COLOR,
            foreground=TEXT_COLOR,
            borderwidth=5,
            relief="solid",
            focusthickness=3,
            focuscolor="none",
            padding=PADDING - 2,
        )
        style.map(
            "Lang.TButton",
            background=[("active", DISPLAY_BG_COLOR)],
            foreground=[("disabled", TEXT_COLOR)],
        )

        # Transaction table
        style.configure(
            "Transaction.Treeview",
            background=DISPLAY_BG_COLOR,
            foreground=TEXT_COLOR,
            rowheight=40,
            fieldbackground=DISPLAY_BG_COLOR,
            font=("Arial", 11),
        )
        style.configure(
            "Transaction.Treeview.Heading",
            background="#000000",
            foreground=TEXT_COLOR,
            font=("Arial", 14, "bold"),
        )

    #################### Create widgets ####################
    # Create main widgets
    def create_widget(self):
        # Create display panel
        self.create_display_panel_widgets(self.root)

        # Create control panel
        self.create_control_panel_widgets(self.root)

    # Create display panel widgets
    def create_display_panel_widgets(self, parent):
        display_panel = Frame(
            parent, bg=DISPLAY_BG_COLOR, width=DISPLAY_PANEL_WIDTH, height=APP_HEIGHT
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

        self.create_title_lang_panel(display_panel)
        self.create_summary_panel(display_panel)
        self.create_transaction_list_panel(display_panel)

    ## Create title and language toggle button panel
    def create_title_lang_panel(self, parent):
        Label(
            parent,
            textvariable=self.title_label,
            bg=DISPLAY_BG_COLOR,
            fg=TEXT_COLOR,
            font=("Times", 30),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=PADDING)
        self.create_button_widgets(
            parent,
            self.lang_label,
            "Lang.TButton",
            10,
            self.toggle_language,
            "grid",
            row=0,
            column=2,
            sticky="e",
            padx=PADDING,
        )

    ## Create summary panel
    def create_summary_panel(self, parent):
        # Income summary widget
        self.create_summary_widgets(
            parent,
            INCOME_COLOR,
            self.total_income_label,
            self.total_income_var,
            row=1,
            column=0,
            sticky="nsew",
            padx=PADDING,
            pady=PADDING + 20,
        )

        # Expense summary widget
        self.create_summary_widgets(
            parent,
            EXPENSE_COLOR,
            self.total_expense_label,
            self.total_expense_var,
            row=1,
            column=1,
            sticky="nsew",
            padx=PADDING,
            pady=PADDING + 20,
        )

        # Balance summary widget
        self.create_summary_widgets(
            parent,
            BALANCE_COLOR,
            self.total_balance_label,
            self.total_balance_var,
            row=1,
            column=2,
            sticky="nsew",
            padx=PADDING,
            pady=PADDING + 20,
        )

    ### Create summary widgets
    def create_summary_widgets(
        self, parent, text_color, head_label, value_label, **options
    ):
        sub_frame = Frame(
            parent,
            bg=DISPLAY_BG_COLOR,
            relief="solid",
            highlightthickness=5,
            highlightbackground=text_color,
            bd=0,
        )
        sub_frame.grid(**options)
        sub_frame.grid_propagate(False)

        Label(
            sub_frame,
            textvariable=head_label,
            bg=DISPLAY_BG_COLOR,
            foreground=TEXT_COLOR,
            font=("Arial", 14),
            padx=PADDING,
            pady=PADDING + 5,
        ).pack(anchor="w")
        Label(
            sub_frame,
            textvariable=value_label,
            bg=DISPLAY_BG_COLOR,
            fg=text_color,
            font=("Arial", 20),
            padx=PADDING,
            pady=PADDING,
        ).pack(anchor="e", expand=True)

    ## Create transaction list panel
    def create_transaction_list_panel(self, parent):
        table_frame = Frame(parent)
        table_frame.grid(
            row=2, column=0, columnspan=3, sticky="nsew", padx=PADDING, pady=PADDING
        )

        columns_name = ("date", "category", "type", "amount", "note")
        self.transaction_table = ttk.Treeview(
            table_frame,
            columns=columns_name,
            show="headings",
            style="Transaction.Treeview",
        )

        self.transaction_table.heading("date", text=self.heading_date_label.get())
        self.transaction_table.heading(
            "category", text=self.heading_category_label.get()
        )
        self.transaction_table.heading("type", text=self.heading_type_label.get())
        self.transaction_table.heading("amount", text=self.heading_amount_label.get())
        self.transaction_table.heading("note", text=self.heading_note_label.get())

        self.transaction_table.column("date", width=80)
        self.transaction_table.column("category", width=100)
        self.transaction_table.column("type", width=80)
        self.transaction_table.column("amount", width=100, anchor="e")
        self.transaction_table.column("note", width=200)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.transaction_table.yview
        )
        self.transaction_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.transaction_table.pack(fill="both", expand=True)

        # Refresh first time
        self.refresh_transaction_table()

    def refresh_transaction_table(self):
        # ลบข้อมูลเก่า
        for row in self.transaction_table.get_children():
            self.transaction_table.delete(row)

        # ใส่ข้อมูลใหม่
        for data in self.loaded_transactions:
            self.transaction_table.insert(
                "",
                "end",
                values=(
                    data["Date"],
                    data["Category"],
                    data["Type"],
                    data["Amount"],
                    data["Note"],
                ),
            )

    # Create control panel widgets
    def create_control_panel_widgets(self, parent):
        control_panel = Frame(
            parent, bg=CONTROL_BG_COLOR, width=CONTROL_PANEL_WIDTH, height=APP_HEIGHT
        )
        control_panel.grid(row=0, column=1, sticky="nsew")
        control_panel.grid_propagate(False)

        # Create control panel tabs
        self.control_panel_tabs = ttk.Notebook(control_panel)
        self.control_panel_tabs.pack(fill="both", expand=True)

        # Create input panel inside control panel
        self.create_input_panel_widgets(self.control_panel_tabs)

        # Create filter panel inside control panel
        # self.create_filter_panel_widgets(self.control_panel_tabs)

        # Style
        style = ttk.Style()
        style.configure("TNotebook", bg=CONTROL_BG_COLOR)

    ## Create input panel widgets
    def create_input_panel_widgets(self, parent):
        # Create input panel inside control panel
        self.input_panel = Frame(parent, bg=CONTROL_BG_COLOR)
        self.input_panel.pack(fill="both", expand=True)
        parent.add(self.input_panel, text=self.add_transaction_label.get())

        # Add widgets in input panel
        self.create_date_input_widgets(
            self.input_panel
        )  # Add date input to input panel
        self.create_income_expense_input_widgets(
            self.input_panel
        )  # Add radio buttons income and expense to input panel
        self.create_category_input_widgets(
            self.input_panel
        )  # Add category input to input panel
        self.create_amount_input_widgets(
            self.input_panel
        )  # Add amount input to input panel
        self.create_note_input_widgets(
            self.input_panel
        )  # Add note input to input panel

        self.create_save_reset_button_widgets(
            self.input_panel
        )  # Add save and reset buttons to input panel

    ### Create date input widgets
    def create_date_input_widgets(self, parent):
        Label(
            parent, textvariable=self.date_label, bg=CONTROL_BG_COLOR, fg=TEXT_COLOR
        ).pack()
        date_input_panel = Frame(parent, bg=CONTROL_BG_COLOR)
        date_input_panel.pack()
        date_input_panel.grid_rowconfigure(0, weight=1)
        for i in range(3):
            date_input_panel.grid_columnconfigure(i, weight=1)

        days = [str(d) for d in range(1, 32)]
        months = [str(m) for m in range(1, 13)]
        years = [str(y) for y in range(2000, datetime.now().year + 1)]

        ttk.Combobox(
            date_input_panel,
            textvariable=self.day_var,
            values=days,
            width=5,
            state="readonly",
        ).grid(row=0, column=0)
        ttk.Combobox(
            date_input_panel,
            textvariable=self.month_var,
            values=months,
            width=5,
            state="readonly",
        ).grid(row=0, column=1)
        ttk.Combobox(
            date_input_panel,
            textvariable=self.year_var,
            values=years,
            width=5,
            state="readonly",
        ).grid(row=0, column=2)

    ### Create income/expense input widgets
    def create_income_expense_input_widgets(self, parent):
        Label(
            parent, textvariable=self.type_label, bg=CONTROL_BG_COLOR, fg=TEXT_COLOR
        ).pack()
        self.income_radio = ttk.Radiobutton(
            parent,
            text=self.get_label("รายรับ", "Income"),
            variable=self.transaction_type_var,
            value="income",
            command=self.get_category_values,
        )
        self.income_radio.pack()
        self.expense_radio = ttk.Radiobutton(
            parent,
            text=self.get_label("รายจ่าย", "Expense"),
            variable=self.transaction_type_var,
            value="expense",
            command=self.get_category_values,
        )
        self.expense_radio.pack()

    ### Create category input widgets
    def create_category_input_widgets(self, parent):
        Label(
            parent, textvariable=self.category_label, bg=CONTROL_BG_COLOR, fg=TEXT_COLOR
        ).pack()
        self.categorie_option = ttk.Combobox(
            parent, textvariable=self.category_var, state="readonly"
        )
        self.get_category_values()
        self.categorie_option.current(0)
        self.categorie_option.pack()

    ### Create amount input widgets
    def create_amount_input_widgets(self, parent):
        Label(
            parent, textvariable=self.amount_label, bg=CONTROL_BG_COLOR, fg=TEXT_COLOR
        ).pack()
        vcmd = (self.root.register(self.validate_amount), "%P")
        Entry(
            parent,
            textvariable=self.amount_var,
            validate="key",
            validatecommand=vcmd,
        ).pack()

    ### Create note input widgets
    def create_note_input_widgets(self, parent):
        Label(
            parent, textvariable=self.note_label, bg=CONTROL_BG_COLOR, fg=TEXT_COLOR
        ).pack()
        self.note_var = Text(parent, height=5, width=40)
        self.note_var.pack()

    ### Create save and reset button widgets
    def create_save_reset_button_widgets(self, parent):
        button_panel = Frame(parent, bg=CONTROL_BG_COLOR)
        button_panel.pack(pady=PADDING)
        button_panel.grid_rowconfigure(0, weight=1)
        button_panel.grid_columnconfigure(0, weight=1)
        button_panel.grid_columnconfigure(1, weight=1)

        # Save button
        self.create_button_widgets(
            button_panel,
            self.save_button_label,
            "Submit.TButton",
            width=10,
            command=self.save_transaction,
            pack_or_grid="grid",
            row=0,
            column=0,
            padx=PADDING,
        )

        # Reset button
        self.create_button_widgets(
            button_panel,
            self.reset_button_label,
            "Normal.TButton",
            10,
            self.reset_fields,
            pack_or_grid="grid",
            row=0,
            column=1,
            padx=PADDING,
        )

    ## Create filter panel widgets
    # def create_filter_panel_widgets(self, parent):
    #     self.filter_panel = Frame(parent, bg="#ff0000")
    #     self.filter_panel.pack(fill="both", expand=True)
    #     parent.add(self.filter_panel, text="Filter")

    ### Create button widgets
    def create_button_widgets(
        self,
        parent,
        text_var,
        style,
        width,
        command,
        pack_or_grid="pack",
        **options,
    ):

        btn = ttk.Button(
            parent,
            textvariable=text_var,
            style=style,
            width=width,
            command=command,
        )

        if pack_or_grid == "pack":
            btn.pack(**options)
        elif pack_or_grid == "grid":
            btn.grid(**options)

    #################### Helper functions ####################

    # Toggle language function
    def toggle_language(self):

        # Toggle between "th" and "en"
        if self.lang_var.get() == "th":
            self.lang_var.set("en")
        else:
            self.lang_var.set("th")

        # Update all labels based on the selected language
        ## Display panel
        ### Heading panel
        self.lang_label.set(self.get_label("English", "Thai"))

        ### Summary panel
        self.total_income_label.set(self.get_label("รายรับทั้งหมด", "Total Income"))
        self.total_expense_label.set(self.get_label("รายจ่ายทั้งหมด", "Total Expense"))
        self.total_balance_label.set(self.get_label("ยอดคงเหลือ", "Total Balance"))

        ### Transaction list panel
        self.heading_date_label.set(self.get_label("วันที่", "Date"))
        self.heading_category_label.set(self.get_label("หมวดหมู่", "Category"))
        self.heading_type_label.set(self.get_label("ประเภท", "Type"))
        self.heading_amount_label.set(self.get_label("จำนวนเงิน", "Amount"))
        self.heading_note_label.set(
            self.get_label("หมายเหตุ (ไม่จำเป็น)", "Note (Optional)")
        )
        self.process_label.set(self.get_label("การดำเนินการ", "Process"))
        self.process_edit_button_label.set(self.get_label("แก้ไข", "Edit"))
        self.process_delete_button_label.set(self.get_label("ลบ", "Delete"))

        ## Control panel
        ### Add transaction panel
        self.add_transaction_label.set(self.get_label("เพิ่มรายการ", "Add Transaction"))
        self.date_label.set(self.get_label("วันที่", "Date"))
        self.type_label.set(self.get_label("ประเภท", "Type"))
        self.income_radio.config(text=self.get_label("รายรับ", "Income"))
        self.expense_radio.config(text=self.get_label("รายจ่าย", "Expense"))
        self.category_label.set(self.get_label("หมวดหมู่", "Category"))
        self.category_input_option_label.set(
            self.get_label("เลือกหมวดหมู่", "Select Category")
        )
        self.amount_label.set(self.get_label("จำนวนเงิน", "Amount"))
        self.note_label.set(self.get_label("หมายเหตุ (ไม่จำเป็น)", "Note (Optional)"))
        self.save_button_label.set(self.get_label("บันทึก", "Save"))
        self.reset_button_label.set(self.get_label("ล้างข้อมูล", "Reset"))

        ### Filter panel
        # self.filter_label.set(self.get_label("ตัวกรอง", "Filter"))
        # self.start_date_filter_label.set(self.get_label("วันที่เริ่มต้น", "Start Date"))
        # self.end_date_filter_label.set(self.get_label("วันที่สิ้นสุด", "End Date"))
        # self.category_filter_option_label.set(self.get_label("ทั้งหมด", "All"))
        # self.apply_filter_button_label.set(self.get_label("ใช้ตัวกรอง", "Apply Filter"))
        # self.clear_filter_button_label.set(self.get_label("ล้างตัวกรอง", "Clear Filter"))
        # self.export_csv_button_label.set(self.get_label("ส่งออก CSV", "Export CSV"))
        # self.export_pdf_button_label.set(self.get_label("ส่งออก PDF", "Export PDF"))
        # self.delete_all_button_label.set(self.get_label("ลบทั้งหมด", "Delete All"))

        self.control_panel_tabs.tab(
            self.input_panel, text=self.add_transaction_label.get()
        )
        # self.control_panel_tabs.tab(self.filter_panel, text=self.filter_label.get())

        self.transaction_table.heading("date", text=self.date_label.get())
        self.transaction_table.heading("category", text=self.category_label.get())
        self.transaction_table.heading("type", text=self.type_label.get())
        self.transaction_table.heading("amount", text=self.amount_label.get())
        self.transaction_table.heading("note", text=self.note_label.get())

        # Update category values in combobox
        self.get_category_values()

    # Helper function to get label based on language
    def get_label(self, th_label, en_label):
        return th_label if self.lang_var.get() == "th" else en_label

    # Get category values based on transaction type and language
    def get_category_values(self):
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

    # Amount validation
    def validate_amount(self, amount):
        if amount == "":
            return True
        try:
            float(amount)
            return True
        except ValueError:
            return False

    # Save transaction
    def save_transaction(self):
        date = datetime(
            int(self.year_var.get()), int(self.month_var.get()), int(self.day_var.get())
        ).strftime("%d-%m-%Y")
        transaction_type = self.transaction_type_var.get()
        category = self.category_var.get()
        amount = self.amount_var.get()
        note = self.note_var.get("1.0", "end").strip()

        if not amount:
            messagebox.showerror(
                self.get_label("ข้อผิดพลาด", "Error"),
                self.get_label("กรุณาใส่จำนวนเงิน", "Please enter an amount"),
            )
            return

        # Save to CSV file
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Category", "Type", "Amount", "Note"])
            writer.writerow([date, category, transaction_type, float(amount), note])

        self.reset_fields()
        self.load_transactions()

    # Reset input fields
    def reset_fields(self):
        self.day_var.set(datetime.now().day)
        self.month_var.set(datetime.now().month)
        self.year_var.set(datetime.now().year)
        self.transaction_type_var.set("income")
        self.get_category_values()
        self.amount_var.set("")
        self.note_var.delete("1.0", "end")

    # Load transactions from CSV file
    def load_transactions(self):
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.loaded_transactions = list(reader)
        self.get_totals()
        self.refresh_transaction_table()

    # Get total income, expense, and balance
    def get_totals(self):
        # Calculate total income
        total_income = sum(
            float(trans["Amount"])
            for trans in self.loaded_transactions
            if trans["Type"] == "income"
        )
        # Calculate total expense
        total_expense = sum(
            float(trans["Amount"])
            for trans in self.loaded_transactions
            if trans["Type"] == "expense"
        )

        # Calculate total balance
        total_balance = total_income - total_expense

        # Update variables
        self.total_income_var.set(f"{total_income:,.2f}")
        self.total_expense_var.set(f"{total_expense:,.2f}")
        self.total_balance_var.set(f"{total_balance:,.2f}")


if __name__ == "__main__":
    root = Tk()
    app = BudgetTracker(root)
    root.mainloop()
