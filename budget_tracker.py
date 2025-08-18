"""
Budget Tracker GUI Application
Author: Kairung Vangmanaw
Date: August 2025
"""

from tkinter import Tk, Frame, Label, Button, Entry, StringVar, messagebox

# Constants for the application
APP_TITLE = "Budget Tracker"
APP_WIDTH = 800
APP_HEIGHT = 500
BG_COLOR = "#212121"  # Background color
FG_COLOR = "#faf9f6"  # Foreground (text) color

import csv
import os
from tkinter import ttk
from datetime import datetime

# CSV file for persistent storage
CSV_FILE = "transactions.csv"


class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Variables
        self.date_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.category_var = StringVar()
        self.desc_var = StringVar()
        self.amount_var = StringVar()
        self.balance_var = StringVar(value="0.00")

        # UI
        self.create_widgets()
        self.load_transactions()
        self.update_balance()

    def create_widgets(self):
        # Input Frame
        input_frame = Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=10)

        Label(input_frame, text="วันที่", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=0, column=0, padx=5, sticky="e"
        )
        Entry(input_frame, textvariable=self.date_var, width=10).grid(
            row=0, column=1, padx=5
        )

        Label(input_frame, text="หมวดหมู่", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=0, column=2, padx=5, sticky="e"
        )
        self.category_cb = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=["อาหาร", "การเดินทาง", "รายรับ", "อื่นๆ"],
            width=10,
        )
        self.category_cb.grid(row=0, column=3, padx=5)
        self.category_cb.set("อาหาร")

        Label(input_frame, text="คำอธิบาย", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=1, column=0, padx=5, sticky="e"
        )
        Entry(input_frame, textvariable=self.desc_var, width=20).grid(
            row=1, column=1, padx=5
        )

        Label(input_frame, text="จำนวนเงิน", bg=BG_COLOR, fg=FG_COLOR).grid(
            row=1, column=2, padx=5, sticky="e"
        )
        Entry(input_frame, textvariable=self.amount_var, width=10).grid(
            row=1, column=3, padx=5
        )

        Button(
            input_frame,
            text="เพิ่มรายการ",
            command=self.add_transaction,
            bg="#388e3c",
            fg=FG_COLOR,
        ).grid(row=2, column=0, columnspan=2, pady=5)
        Button(
            input_frame,
            text="ลบรายการ",
            command=self.delete_transaction,
            bg="#d32f2f",
            fg=FG_COLOR,
        ).grid(row=2, column=2, columnspan=2, pady=5)

        # Table Frame
        table_frame = Frame(self.root, bg=BG_COLOR)
        table_frame.pack(pady=5, fill="both", expand=True)

        columns = ("date", "category", "desc", "amount")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=7
        )
        self.tree.heading("date", text="วันที่")
        self.tree.heading("category", text="หมวดหมู่")
        self.tree.heading("desc", text="คำอธิบาย")
        self.tree.heading("amount", text="จำนวนเงิน")
        self.tree.column("amount", anchor="e", width=80)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Summary Frame
        summary_frame = Frame(self.root, bg=BG_COLOR)
        summary_frame.pack(pady=5, fill="x")
        Label(summary_frame, text="ยอดคงเหลือ:", bg=BG_COLOR, fg=FG_COLOR).pack(
            side="left"
        )
        Label(
            summary_frame,
            textvariable=self.balance_var,
            bg=BG_COLOR,
            fg=FG_COLOR,
            font=("Arial", 12, "bold"),
        ).pack(side="left")
        Button(
            summary_frame,
            text="สรุปยอด",
            command=self.show_summary,
            bg="#1976d2",
            fg=FG_COLOR,
        ).pack(side="right")

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
        self.tree.insert("", "end", values=(date, category, desc, amount))
        self.update_balance()
        self.clear_inputs()

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกรายการที่ต้องการลบ")
            return
        for item in selected:
            values = self.tree.item(item, "values")
            self.tree.delete(item)
            self.remove_from_csv(values)
        self.update_balance()

    def remove_from_csv(self, values):
        # Remove the row from CSV by rewriting the file
        rows = []
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row != list(values):
                    rows.append(row)
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def load_transactions(self):
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                pass
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    self.tree.insert("", "end", values=row)

    def update_balance(self):
        total = 0.0
        for row in self.tree.get_children():
            amount = float(self.tree.item(row, "values")[3])
            category = self.tree.item(row, "values")[1]
            if category == "รายรับ":
                total += amount
            else:
                total -= amount
        self.balance_var.set(f"{total:,.2f}")

    def clear_inputs(self):
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.category_cb.set("อาหาร")
        self.desc_var.set("")
        self.amount_var.set("")

    def show_summary(self):
        # Summarize by category
        summary = {}
        for row in self.tree.get_children():
            category = self.tree.item(row, "values")[1]
            amount = float(self.tree.item(row, "values")[3])
            if category == "รายรับ":
                summary.setdefault(category, 0)
                summary[category] += amount
            else:
                summary.setdefault(category, 0)
                summary[category] -= amount
        msg = ""
        for cat, amt in summary.items():
            msg += f"{cat}: {amt:,.2f}\n"
        messagebox.showinfo("สรุปยอดตามหมวดหมู่", msg)


if __name__ == "__main__":
    root = Tk()
    app = BudgetTracker(root)
    root.mainloop()
