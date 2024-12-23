import tkinter as tk


def get_screen_size() -> tuple[int, int]:
    # cross-platform easy way
    root = tk.Tk()
    sys_width = root.winfo_screenwidth()
    sys_height = root.winfo_screenheight()
    root.destroy()

    return sys_width, sys_height
