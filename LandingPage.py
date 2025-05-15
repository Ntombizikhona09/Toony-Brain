import tkinter as tk
from tkinter import Entry, Button, Label, PhotoImage

def create_ui():
    root = tk.Tk()
    root.title("Toony Brain Siya")
    root.geometry("600x400")
    root.configure(bg='purple')

    # Welcome Label
    welcome_label = Label(root, text="Welcome to Toony Brain Siya!", font=("Arial", 24), bg='purple', fg='white')
    welcome_label.pack(pady=20)

    # Profile Selection Frame
    profile_frame = tk.Frame(root, bg='purple')
    profile_frame.pack(pady=10)

    # Load Profile Images
    smiley_img = PhotoImage(file="smiley.png")  # Replace with actual path
    hello_kitty_img = PhotoImage(file="hello_kitty.png")  # Replace with actual path

    smiley_button = Button(profile_frame, image=smiley_img, bg='yellow')
    smiley_button.grid(row=0, column=0, padx=20)

    hello_kitty_button = Button(profile_frame, image=hello_kitty_img, bg='pink')
    hello_kitty_button.grid(row=0, column=1, padx=20)

    choose_label = Label(profile_frame, text="Choose a profile:", font=("Arial", 16), bg='purple', fg='white')
    choose_label.grid(row=1, columnspan=2, pady=10)

    # Input Fields Frame
    input_frame = tk.Frame(root, bg='purple')
    input_frame.pack(pady=10)

    Label(input_frame, text="Name :", font=("Arial", 14), bg='purple', fg='white').grid(row=0, column=0, padx=10, pady=5)
    name_entry = Entry(input_frame, font=("Arial", 14))
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_frame, text="Surname :", font=("Arial", 14), bg='purple', fg='white').grid(row=1, column=0, padx=10, pady=5)
    surname_entry = Entry(input_frame, font=("Arial", 14))
    surname_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(input_frame, text="Date of Birth :", font=("Arial", 14), bg='purple', fg='white').grid(row=2, column=0, padx=10, pady=5)
    dob_entry = Entry(input_frame, font=("Arial", 14))
    dob_entry.grid(row=2, column=1, padx=10, pady=5)

    # Start Button
    start_button = Button(root, text="Start", font=("Arial", 14), bg='green', fg='white')
    start_button.pack(pady=20)

    # Tweety Bird Image
    tweety_img = PhotoImage(file="tweety.png")  # Replace with actual path
    tweety_label = Label(root, image=tweety_img, bg='purple')
    tweety_label.pack(side=tk.RIGHT, padx=20)

    root.mainloop()

create_ui()
