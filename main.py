import tkinter as tk
from tkinter import ttk
import datetime
# -------- DATA STORAGE (AP CSP LIST) --------
assignments = []
WARNING = "⚠"
UNCHECKED = "☐"
CHECKED = "✔"
# -------- DATE VALIDATION PROCEDURE --------
def validate_due_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%m/%d/%y").date()
    except ValueError:
        return None
# -------- STUDENT-DEVELOPED PROCEDURE --------
# Contains sequencing, selection, iteration
def check_due_warning(assignments_list):
    today = datetime.date.today()
    processed = []
    for task, due_date in assignments_list:      
        days_left = (due_date - today).days        

        if days_left <= 1:                        
            status = WARNING
        else:
            status = UNCHECKED

        processed.append([task, due_date, status])
    return processed


# -------- DISPLAY ASSIGNMENTS --------
def display_assignments():

    for item in tree.get_children():
        tree.delete(item)

    processed = check_due_warning(assignments)

    for task, due_date, status in processed:
        tree.insert("", "end",
                    text=status,
                    values=(task, due_date.strftime("%m/%d/%y")))


# -------- ADD ASSIGNMENT --------
def add_assignment():
    name = assignment_entry.get()
    date_text = due_entry.get()

    due_date = validate_due_date(date_text)

    if due_date is None:
        print("Invalid date. Use MM/DD/YY")
        return

    assignments.append([name, due_date])

    assignment_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)

    display_assignments()


# -------- SORT BY DUE DATE --------
def sort_due_date():

    assignments.sort(key=lambda x: x[1])
    display_assignments()


# -------- TOGGLE CHECKBOX --------
def toggle_checkbox(event):

    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    if item and column == "#0":

        current = tree.item(item, "text")

        if current == CHECKED:
            tree.item(item, text=UNCHECKED)
        else:
            tree.item(item, text=CHECKED)


# -------- GUI --------
root = tk.Tk()
root.title("Homework Tracker")
root.geometry("500x500")
root.configure(padx=20, pady=20)

tree = ttk.Treeview(root, columns=("task", "due"))

tree.heading("#0", text="Done")
tree.heading("task", text="Assignment/Test Name")
tree.heading("due", text="Due Date")

tree.column("#0", width=80, anchor="center")
tree.column("task", width=280, anchor="center")
tree.column("due", width=100, anchor="center")

tree.pack(pady=10)

tree.bind("<Button-1>", toggle_checkbox)

# -------- INPUT AREA --------
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Assignment/Test Name").grid(row=0, column=0, pady=5)

assignment_entry = tk.Entry(input_frame)
assignment_entry.grid(row=0, column=1, padx=10)

tk.Label(input_frame, text="Due Date (MM/DD/YY)").grid(row=1, column=0, pady=5)

due_entry = tk.Entry(input_frame)
due_entry.grid(row=1, column=1, padx=10)

tk.Button(input_frame,
          text="Add Assignment",
          command=add_assignment).grid(row=2, column=1, pady=5)

tk.Button(input_frame,
          text="Sort by Due Date",
          command=sort_due_date).grid(row=3, column=1, pady=5)

root.mainloop()