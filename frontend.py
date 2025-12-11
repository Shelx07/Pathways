# frontend.py
import tkinter as tk
from tkinter import ttk, messagebox
import backend

# -------------------------
# Basic setup
# -------------------------

backend.ensure_file_exists()

root = tk.Tk()
root.title("Library Manager")
root.geometry("640x420")
root.resizable(True, True)

style = ttk.Style(root)
try:
    style.theme_use("clam")
except Exception:
    pass

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill="both")

title = ttk.Label(main_frame, text="Pathways", font=("Helvetica", 20, "bold"))
title.pack(pady=(0, 12))

subtitle = ttk.Label(main_frame, text="Welcome to Pathways", font=("Helvetica", 10))
subtitle.pack(pady=(0, 18))

btn_frame = ttk.Frame(main_frame)
btn_frame.pack()

def center_children(frame):
    for child in frame.winfo_children():
        child.pack_configure(anchor="center")

# -------------------------
# Create Account Window
# -------------------------
def open_create_account():
    win = tk.Toplevel(root)
    win.title("Create Account")
    win.geometry("420x260")
    win.resizable(False, False)

    frm = ttk.Frame(win, padding=16)
    frm.pack(expand=True, fill="both")

    ttk.Label(frm, text="Create New Account", font=("Helvetica", 14, "bold")).pack(pady=(0,10))

    ttk.Label(frm, text="User ID").pack(anchor="w", pady=(6,0))
    user_entry = ttk.Entry(frm, width=40)
    user_entry.pack()

    ttk.Label(frm, text="Password").pack(anchor="w", pady=(8,0))
    pass_entry = ttk.Entry(frm, width=40, show="*")
    pass_entry.pack()

    ttk.Label(frm, text="Confirm Password").pack(anchor="w", pady=(8,0))
    pass_confirm = ttk.Entry(frm, width=40, show="*")
    pass_confirm.pack()

    def create_action():
        uid = user_entry.get().strip()
        pw = pass_entry.get().strip()
        pwc = pass_confirm.get().strip()
        if not uid or not pw:
            messagebox.showwarning("Missing data", "Please enter both user id and password.")
            return
        if pw != pwc:
            messagebox.showerror("Mismatch", "Password and confirm do not match.")
            return
        ok, msg = backend.create_account(uid, pw)
        if ok:
            messagebox.showinfo("Success", msg)
            win.destroy()
        else:
            messagebox.showerror("Error", msg)

    ttk.Button(frm, text="Create Account", command=create_action).pack(pady=(12,5))
    ttk.Button(frm, text="Cancel", command=win.destroy).pack()

# -------------------------
# Add Books Window
# -------------------------
def open_add_books():
    win = tk.Toplevel(root)
    win.title("Add Books")
    win.geometry("480x340")
    win.resizable(False, False)

    frm = ttk.Frame(win, padding=16)
    frm.pack(expand=True, fill="both")

    ttk.Label(frm, text="Add Book(s) to Account", font=("Helvetica", 14, "bold")).pack(pady=(0,10))

    ttk.Label(frm, text="User ID").pack(anchor="w", pady=(6,0))
    user_entry = ttk.Entry(frm, width=45)
    user_entry.pack()

    ttk.Label(frm, text="Password").pack(anchor="w", pady=(8,0))
    pass_entry = ttk.Entry(frm, width=45, show="*")
    pass_entry.pack()

    ttk.Label(frm, text="Book names (comma-separated)").pack(anchor="w", pady=(8,0))
    books_entry = ttk.Entry(frm, width=60)
    books_entry.pack()

    current_label = ttk.Label(frm, text="")
    current_label.pack(pady=(8,0))

    def refresh_current():
        uid = user_entry.get().strip()
        pw = pass_entry.get().strip()
        if not uid or not pw:
            current_label.config(text="")
            return
        r = backend.get_user(uid, pw)
        if r:
            current_label.config(text=f"Currently borrowed: {len(r['books'])} books")
        else:
            current_label.config(text="User not found")

    user_entry.bind("<FocusOut>", lambda e: refresh_current())
    pass_entry.bind("<FocusOut>", lambda e: refresh_current())

    def add_action():
        uid = user_entry.get().strip()
        pw = pass_entry.get().strip()
        raw = books_entry.get().strip()
        if not uid or not pw or not raw:
            messagebox.showwarning("Missing data", "Fill user, password and at least one book name.")
            return
        new_books = [b.strip() for b in raw.split(",") if b.strip()]
        ok, msg = backend.add_books(uid, pw, new_books)
        if ok:
            messagebox.showinfo("Success", msg)
            win.destroy()
        else:
            messagebox.showerror("Error", msg)

    ttk.Button(frm, text="Add Books", command=add_action).pack(pady=(12,6))
    ttk.Button(frm, text="Cancel", command=win.destroy).pack()

# -------------------------
# View Record Window
# -------------------------
def open_view_record():
    win = tk.Toplevel(root)
    win.title("View Record")
    win.geometry("520x360")
    win.resizable(False, False)

    frm = ttk.Frame(win, padding=12)
    frm.pack(expand=True, fill="both")

    ttk.Label(frm, text="View User Record", font=("Helvetica", 14, "bold")).pack(pady=(0,8))

    ttk.Label(frm, text="User ID").pack(anchor="w")
    user_entry = ttk.Entry(frm, width=40)
    user_entry.pack()

    ttk.Label(frm, text="Password").pack(anchor="w", pady=(8,0))
    pass_entry = ttk.Entry(frm, width=40, show="*")
    pass_entry.pack()

    def view_action():
        uid = user_entry.get().strip()
        pw = pass_entry.get().strip()
        if not uid or not pw:
            messagebox.showwarning("Missing data", "Enter user id and password.")
            return
        r = backend.get_user(uid, pw)
        if r is None:
            messagebox.showerror("Not found", "User ID or password incorrect.")
            return
        details = tk.Toplevel(win)
        details.title(f"Record: {uid}")
        details.geometry("420x320")
        dfrm = ttk.Frame(details, padding=10)
        dfrm.pack(expand=True, fill="both")
        ttk.Label(dfrm, text=f"User ID: {r['user']}", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0,6))
        ttk.Label(dfrm, text=f"Books Borrowed: {len(r['books'])}").pack(anchor="w", pady=(0,8))
        ttk.Label(dfrm, text="Book List:", font=("Helvetica", 10, "underline")).pack(anchor="w")
        listbox = tk.Listbox(dfrm, height=10, width=50)
        listbox.pack(pady=(6,0))
        for b in r['books']:
            listbox.insert(tk.END, b)
        ttk.Button(dfrm, text="Close", command=details.destroy).pack(pady=(10,0))

    ttk.Button(frm, text="View Record", command=view_action).pack(pady=(12,6))
    ttk.Button(frm, text="Cancel", command=win.destroy).pack()

# -------------------------
# Return Book Window
# -------------------------
def open_return_book():
    win = tk.Toplevel(root)
    win.title("Return Books")
    win.geometry("560x420")
    win.resizable(False, False)

    frm = ttk.Frame(win, padding=12)
    frm.pack(expand=True, fill="both")

    ttk.Label(frm, text="Return Book(s)", font=("Helvetica", 14, "bold")).pack(pady=(0,6))

    ttk.Label(frm, text="User ID").pack(anchor="w")
    user_entry = ttk.Entry(frm, width=40)
    user_entry.pack()

    ttk.Label(frm, text="Password").pack(anchor="w", pady=(8,0))
    pass_entry = ttk.Entry(frm, width=40, show="*")
    pass_entry.pack()

    ttk.Label(frm, text="(After login, select book(s) below and click 'Return Selected')", font=("Helvetica", 9)).pack(pady=(8,6))

    listbox = tk.Listbox(frm, selectmode=tk.MULTIPLE, height=10, width=65)
    listbox.pack()

    def load_books():
        listbox.delete(0, tk.END)
        uid = user_entry.get().strip()
        pw = pass_entry.get().strip()
        if not uid or not pw:
            messagebox.showwarning("Missing data", "Please enter user id and password first.")
            return
        r = backend.get_user(uid, pw)
        if r is None:
            messagebox.showerror("Not found", "User ID or password incorrect.")
            return
        if not r['books']:
            messagebox.showinfo("No books", "This user has no borrowed books.")
            return
        for b in r['books']:
            listbox.insert(tk.END, b)

    def return_selected():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Select", "Select one or more books to return.")
            return
        uid = user_entry.get().strip()
        pw = pass_entry.get().strip()
        picked = [listbox.get(i) for i in sel]
        num, msg = backend.return_books(uid, pw, picked)
        if num is None:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Returned", msg)
            win.destroy()

    ttk.Button(frm, text="Load Borrowed Books", command=load_books).pack(pady=(8,6))
    ttk.Button(frm, text="Return Selected", command=return_selected).pack(pady=(6,4))
    ttk.Button(frm, text="Cancel", command=win.destroy).pack()

# -------------------------
# Main menu buttons
# -------------------------
b1 = ttk.Button(btn_frame, text="Create Account", width=30, command=open_create_account)
b2 = ttk.Button(btn_frame, text="Add Books", width=30, command=open_add_books)
b3 = ttk.Button(btn_frame, text="View Record", width=30, command=open_view_record)
b4 = ttk.Button(btn_frame, text="Return Books", width=30, command=open_return_book)
b5 = ttk.Button(btn_frame, text="Exit", width=30, command=root.quit)

b1.pack(pady=6)
b2.pack(pady=6)
b3.pack(pady=6)
b4.pack(pady=6)
b5.pack(pady=8)

center_children(btn_frame)

root.mainloop()
