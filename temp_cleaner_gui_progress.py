import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import getpass
import threading
import ctypes  # ✅ For admin check

# 📁 Folders to clean
def get_clean_targets():
    user = getpass.getuser()
    return [
        os.environ.get("TEMP"),                            # %TEMP%
        f"C:/Users/{user}/AppData/Local/Temp",            # App temp
        "C:/Windows/Temp",                                # System temp
        "C:/Windows/Prefetch",                            # Prefetch
    ]

# 📦 Count total items
def count_total_items(targets):
    total = 0
    for path in targets:
        if not os.path.exists(path):
            continue
        for _, dirs, files in os.walk(path):
            total += len(dirs) + len(files)
    return total

# 🧽 Clean files/folders with progress
def clean_folders():
    threading.Thread(target=_clean_folders_thread).start()

def _clean_folders_thread():
    deleted = 0
    errors = 0
    targets = get_clean_targets()
    total_items = count_total_items(targets)
    cleaned_items = 0

    if total_items == 0:
        messagebox.showinfo("Done ✅", "No junk files found.")
        return

    for path in targets:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                    deleted += 1
                except:
                    errors += 1
                cleaned_items += 1
                update_progress(cleaned_items, total_items)

            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path, ignore_errors=True)
                    deleted += 1
                except:
                    errors += 1
                cleaned_items += 1
                update_progress(cleaned_items, total_items)

    progress_bar['value'] = 100
    percent_label.config(text="100%")
    messagebox.showinfo("Done ✅", f"Cleaned {deleted} items\nErrors: {errors}")

def update_progress(current, total):
    percent = int((current / total) * 100)
    progress_bar['value'] = percent
    percent_label.config(text=f"{percent}%")
    app.update_idletasks()

# 🔒 Admin check
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 🖥️ GUI Setup
app = tk.Tk()
app.title("🧹 Advanced Temp File Cleaner")
app.geometry("380x300")
app.resizable(False, False)

tk.Label(app, text="🧼 Clean System Junk", font=("Segoe UI", 16, "bold")).pack(pady=10)
tk.Label(app, text="Cleans: %TEMP%, AppData\\Temp, Windows\\Temp, Prefetch").pack()

tk.Button(app, text="🚀 Clean Now", font=("Segoe UI", 13), bg="green", fg="white",
          command=clean_folders).pack(pady=20)

# 🔄 Progress Bar
progress_bar = ttk.Progressbar(app, length=250, mode='determinate')
progress_bar.pack(pady=10)

percent_label = tk.Label(app, text="0%", font=("Segoe UI", 12))
percent_label.pack()

# ✅ Dynamic Admin Status Label
admin_status = is_admin()
admin_text = "✅ NICE YOU RUN AS ADMINISTRATOR" if admin_status else "⚠️ Run as Administrator for full access"
admin_color = "green" if admin_status else "red"

admin_label = tk.Label(app, text=admin_text, fg=admin_color, font=("Segoe UI", 10))
admin_label.pack(pady=10)

app.mainloop()
