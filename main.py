import tkinter as tk

window = tk.Tk()
window.title("Tkinter Test")
window.geometry("300x200")

label = tk.Label(window, text="Tkinter is working!")
label.pack(pady=50)

window.mainloop()
