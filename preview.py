"""
Budget Tracker GUI Application
Author: Kairung Vangmanaw
Date: August 2025
"""

from tkinter import Tk, Frame, Label, Button, Entry, StringVar, messagebox
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import csv, os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants for the application
APP_TITLE = "Budget Tracker"
APP_WIDTH = 1000
APP_HEIGHT = 600
BG_COLOR = "#212121"
FG_COLOR = "#faf9f6"
CSV_FILE = "transactions.csv"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.configure(bg=BG_COLOR)

        # Nav bar
        self.nav_frame = tk.Frame(self, bg="#181818", width=70, height=APP_HEIGHT)
        self.nav_frame.pack(side="left", fill="y")
        self.nav_frame.pack_propagate(False)

        # Container for pages
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(side="left", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, TransactionPage, ReportPage, SettingPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Nav buttons
        nav_buttons = [
            ("🏠", "HomePage"),
            ("📒", "TransactionPage"),
            ("📊", "ReportPage"),
            ("⚙️", "SettingPage"),
        ]
        for i, (icon, page_name) in enumerate(nav_buttons):
            btn = tk.Button(
                self.nav_frame,
                text=icon,
                font=("Arial", 18),
                fg=FG_COLOR,
                bg="#181818",
                bd=0,
                relief="flat",
                activebackground="#333333",
                activeforeground=FG_COLOR,
                command=lambda p=page_name: self.show_frame(p),
            )
            btn.pack(pady=(30 if i == 0 else 10, 0), ipadx=5, ipady=5)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        label = tk.Label(
            self, text="Dashboard", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 24, "bold")
        )
        label.pack(pady=20)

        # Dashboard summary
        self.balance_var = tk.StringVar(value="0.00")
        self.income_var = tk.StringVar(value="0.00")
        self.expense_var = tk.StringVar(value="0.00")

        dash_frame = tk.Frame(self, bg=BG_COLOR)
        dash_frame.pack(pady=10)

        # Balance
        bal_box = tk.Frame(dash_frame, bg="#263238", width=220, height=100)
        bal_box.pack(side="left", padx=20)
        bal_box.pack_propagate(False)
        tk.Label(
            bal_box,
            text="ยอดคงเหลือ",
            bg="#263238",
            fg="#ffd600",
            font=("Arial", 14, "bold"),
        ).pack(pady=(15, 0))
        tk.Label(
            bal_box,
            textvariable=self.balance_var,
            bg="#263238",
            fg="#ffd600",
            font=("Arial", 20, "bold"),
        ).pack()

        # Income
        inc_box = tk.Frame(dash_frame, bg="#1b5e20", width=180, height=100)
        inc_box.pack(side="left", padx=20)
        inc_box.pack_propagate(False)
        tk.Label(
            inc_box, text="รายรับรวม", bg="#1b5e20", fg="#fffde7", font=("Arial", 13)
        ).pack(pady=(15, 0))
        tk.Label(
            inc_box,
            textvariable=self.income_var,
            bg="#1b5e20",
            fg="#fffde7",
            font=("Arial", 18, "bold"),
        ).pack()

        # Expense
        exp_box = tk.Frame(dash_frame, bg="#b71c1c", width=180, height=100)
        exp_box.pack(side="left", padx=20)
        exp_box.pack_propagate(False)
        tk.Label(
            exp_box, text="รายจ่ายรวม", bg="#b71c1c", fg="#fffde7", font=("Arial", 13)
        ).pack(pady=(15, 0))
        tk.Label(
            exp_box,
            textvariable=self.expense_var,
            bg="#b71c1c",
            fg="#fffde7",
            font=("Arial", 18, "bold"),
        ).pack()

        # Chart Frame
        chart_frame = tk.Frame(self, bg=BG_COLOR)
        chart_frame.pack(pady=10, fill="both", expand=True)

        # Pie Chart (รายรับ vs รายจ่าย)
        pie_fig, pie_ax = plt.subplots(figsize=(3, 3), dpi=90)
        self.pie_canvas = FigureCanvasTkAgg(pie_fig, master=chart_frame)
        self.pie_canvas.get_tk_widget().pack(side="left", padx=30)
        self.pie_ax = pie_ax
        self.pie_fig = pie_fig

        # Bar Chart (รายรับ/รายจ่ายรายเดือน)
        bar_fig, bar_ax = plt.subplots(figsize=(4.5, 3), dpi=90)
        self.bar_canvas = FigureCanvasTkAgg(bar_fig, master=chart_frame)
        self.bar_canvas.get_tk_widget().pack(side="left", padx=30)
        self.bar_ax = bar_ax
        self.bar_fig = bar_fig

        self.update_dashboard()

    def update_dashboard(self):
        income = 0.0
        expense = 0.0
        # For bar chart
        month_income = {}
        month_expense = {}
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 4:
                        try:
                            amt = float(row[3])
                        except ValueError:
                            continue
                        # Month key
                        try:
                            month = row[0][:7]  # YYYY-MM
                        except Exception:
                            month = "Unknown"
                        if row[1] == "รายรับ":
                            income += amt
                            month_income[month] = month_income.get(month, 0) + amt
                        else:
                            expense += amt
                            month_expense[month] = month_expense.get(month, 0) + amt
        balance = income - expense
        self.balance_var.set(f"{balance:,.2f}")
        self.income_var.set(f"{income:,.2f}")
        self.expense_var.set(f"{expense:,.2f}")

        # --- Pie Chart ---
        self.pie_ax.clear()
        pie_labels = ["รายรับ", "รายจ่าย"]
        pie_values = [income, expense]
        colors = ["#43a047", "#e53935"]
        if income == 0 and expense == 0:
            self.pie_ax.text(0.5, 0.5, "No Data", ha="center", va="center", fontsize=14)
        else:
            self.pie_ax.pie(
                pie_values,
                labels=pie_labels,
                autopct="%1.1f%%",
                colors=colors,
                startangle=90,
            )
        self.pie_ax.set_title("สัดส่วนรายรับ/รายจ่าย")
        self.pie_fig.tight_layout()
        self.pie_canvas.draw()

        # --- Bar Chart ---
        self.bar_ax.clear()
        months = sorted(set(list(month_income.keys()) + list(month_expense.keys())))
        income_vals = [month_income.get(m, 0) for m in months]
        expense_vals = [month_expense.get(m, 0) for m in months]
        x = range(len(months))
        self.bar_ax.bar(
            x, income_vals, width=0.4, label="รายรับ", color="#43a047", align="center"
        )
        self.bar_ax.bar(
            x, expense_vals, width=0.4, label="รายจ่าย", color="#e53935", align="edge"
        )
        self.bar_ax.set_xticks(x)
        self.bar_ax.set_xticklabels(months, rotation=30, ha="right")
        self.bar_ax.set_ylabel("จำนวนเงิน")
        self.bar_ax.set_title("รายรับ/รายจ่ายรายเดือน")
        self.bar_ax.legend()
        self.bar_fig.tight_layout()
        self.bar_canvas.draw()


class TransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        label = tk.Label(
            self, text="บันทึกรายรับ-รายจ่าย", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 20)
        )
        label.pack(pady=20)

        # Variables
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.category_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        # Input Frame
        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="วันที่", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=0, column=0, padx=5, sticky="e"
        )
        tk.Entry(input_frame, textvariable=self.date_var, width=12).grid(
            row=0, column=1, padx=5
        )

        tk.Label(input_frame, text="หมวดหมู่", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=0, column=2, padx=5, sticky="e"
        )
        self.category_cb = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=["อาหาร", "การเดินทาง", "รายรับ", "อื่นๆ"],
            width=12,
        )
        self.category_cb.grid(row=0, column=3, padx=5)
        self.category_cb.set("อาหาร")

        tk.Label(input_frame, text="คำอธิบาย", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=1, column=0, padx=5, sticky="e"
        )
        tk.Entry(input_frame, textvariable=self.desc_var, width=20).grid(
            row=1, column=1, padx=5
        )

        tk.Label(input_frame, text="จำนวนเงิน", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=1, column=2, padx=5, sticky="e"
        )
        tk.Entry(input_frame, textvariable=self.amount_var, width=12).grid(
            row=1, column=3, padx=5
        )

        tk.Button(
            input_frame,
            text="เพิ่มรายการ",
            command=self.add_transaction,
            bg="#388e3c",
            fg=FG_COLOR,
        ).grid(row=2, column=0, columnspan=4, pady=10)

    def add_transaction(self):
        date = self.date_var.get()
        category = self.category_var.get()
        desc = self.desc_var.get()
        amount = self.amount_var.get()
        try:
            amount_f = float(amount)
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนเงินเป็นตัวเลข")
            return
        if not date or not category or not desc:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return
        # Save to CSV
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, desc, amount])
        messagebox.showinfo("สำเร็จ", "เพิ่มรายการเรียบร้อยแล้ว")
        self.clear_inputs()

    def clear_inputs(self):
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.category_cb.set("อาหาร")
        self.desc_var.set("")
        self.amount_var.set("")


class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        label = tk.Label(
            self, text="Report", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 20)
        )
        label.pack(pady=30)


class SettingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        label = tk.Label(
            self, text="Setting", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 20)
        )
        label.pack(pady=30)


if __name__ == "__main__":
    app = App()
    app.mainloop()
