import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length=12, include_alpha=True, include_numeric=True, include_special=True):
    chars = ""
    if include_alpha:
        chars += string.ascii_letters
    if include_numeric:
        chars += string.digits
    if include_special:
        chars += '@#$&*_'

    if not chars:
        raise ValueError("At least one character set must be included in the password")

    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def password_visible():
    global pw_visible
    pw_visible = not pw_visible
    if pw_visible:
        password_entry.config(show="")
        show_butn.config(text="Hide Password")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    else:
        password_entry.config(show="*")
        show_butn.config(text="Show Password")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, '*' * len(password))

def generate_pw_butn():
    try:
        length = int(length_entry.get())
        if length <= 0:
            messagebox.showerror("Error", "Password length should be greater than 0.")
        else:
            global password, pw_visible
            include_alpha = alpha_var.get()
            include_numeric = numeric_var.get()
            include_special = special_var.get()
            password = generate_password(length, include_alpha, include_numeric, include_special)
            password_entry.delete(0, tk.END)
            password_entry.insert(0, '*' * len(password))
            show_butn.config(state='normal')
            pw_visible = False
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def exit_app():
    root.quit()

def setup_gui():
    root = tk.Tk()
    root.title("Password Generator")

    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    length_label = tk.Label(root, text="Enter Password Length:",fg="brown" ,font=("Arial", 15, "bold"))
    length_label.grid(row=0, column=0, sticky="w")

    length_entry = tk.Entry(root)
    length_entry.grid(row=0, column=1, sticky="e")

    alpha_var = tk.BooleanVar()
    alpha_check = tk.Checkbutton(root, text="Include Alphabetic", variable=alpha_var,fg="darkblue",font=("Arial", 15, "bold"))
    alpha_check.grid(row=1, column=0, columnspan=2, sticky="w")
    alpha_check.select()  # Default to including alphabetic characters

    numeric_var = tk.BooleanVar()
    numeric_check = tk.Checkbutton(root, text="Include Numeric", variable=numeric_var,fg="darkblue",font=("Arial", 15, "bold"))
    numeric_check.grid(row=1, column=1, columnspan=2, sticky="w")
    numeric_check.select()  # Default to including numeric characters

    special_var = tk.BooleanVar()
    special_check = tk.Checkbutton(root, text="Include Special Symbols", variable=special_var,fg="darkblue",font=("Arial", 15, "bold"))
    special_check.grid(row=2, column=0, columnspan=2, sticky="w")
    special_check.select()  # Default to including special symbols

    generate_butn = tk.Button(root, text="Generate Password", command=generate_pw_butn,fg ="red", font=("Arial", 15, "bold"))
    generate_butn.grid(row=4, column=0, columnspan=2, sticky="w")

    password_entry = tk.Entry(root, show="")
    password_entry.grid(row=4, column=1, columnspan=2, sticky="w")

    show_butn = tk.Button(root, text='Show Password', command=password_visible, state="disabled",fg="purple", font=("Arial", 15, "bold"))
    show_butn.grid(row=7, column=0, columnspan=2)


    exit_button = tk.Button(root, text="Exit", command=exit_app, fg="red", font=("Arial", 15, "bold"))
    exit_button.grid(row=8, column=0, columnspan=2)

    return root, length_entry, alpha_var, numeric_var, special_var, password_entry, show_butn

if __name__ == "__main__":
    root, length_entry, alpha_var, numeric_var, special_var, password_entry, show_butn = setup_gui()
    pw_visible = False
    root.mainloop()
