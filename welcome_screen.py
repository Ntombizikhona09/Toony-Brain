import tkinter as tk
from tkinter import Entry, Button, Label, Frame
from PIL import Image, ImageTk

def toggle_inputs():
    """ Toggle input field visibility when an image is clicked """
    global input_visible
    if input_visible:
        input_frame.pack_forget()  # Hide input fields
        start_button.pack_forget()  # Hide Start button as well
    else:
        input_frame.pack(pady=10)  # Show input fields correctly centered
        start_button.pack(pady=15)  # Move Start button below input fields when visible
    input_visible = not input_visible  

def create_ui():
    global input_frame, input_visible, start_button  
    input_visible = False  

    root = tk.Tk()
    root.title("Toony Brain ")
    root.geometry("600x450")  
    root.configure(bg='purple')

    # ✅ Main container frame to center content
    main_frame = Frame(root, bg="purple")
    main_frame.pack(expand=True)  # Pushes elements toward the middle

    # ✅ Heading (Centered & Lowered)
    welcome_label = Label(main_frame, text="Welcome to Toony Brain!", font=("Arial", 24), bg='purple', fg='white')
    welcome_label.pack(pady=20)

    # ✅ Profile Label (Lowered)
    choose_label = Label(main_frame, text="Choose a profile:", font=("Arial", 16), bg='purple', fg='white')
    choose_label.pack(pady=10)

    # ✅ Profile Selection Frame (Centered images)
    profile_frame = Frame(main_frame, bg='purple')
    profile_frame.pack(pady=15)

    try:
        smiley_img = Image.open("assets/spunge.png").resize((130, 130), Image.Resampling.LANCZOS)
        smiley_img = ImageTk.PhotoImage(smiley_img)
    except Exception as e:
        print(f"Error loading spunge image: {e}")
        smiley_img = None  

    try:
        hello_kitty_img = Image.open("assets/hello-kitty-wallpaper-37_605.webp").resize((130, 130), Image.Resampling.LANCZOS)
        hello_kitty_img = ImageTk.PhotoImage(hello_kitty_img)
    except Exception as e:
        print(f"Error loading Hello Kitty image: {e}")
        hello_kitty_img = None  

    smiley_button = Button(profile_frame, image=smiley_img, bg='yellow', command=toggle_inputs) if smiley_img else Button(profile_frame, text="Spunge", command=toggle_inputs)
    smiley_button.grid(row=0, column=0, padx=20)

    hello_kitty_button = Button(profile_frame, image=hello_kitty_img, bg='pink', command=toggle_inputs) if hello_kitty_img else Button(profile_frame, text="Hello Kitty", command=toggle_inputs)
    hello_kitty_button.grid(row=0, column=1, padx=20)  

    # ✅ Input Fields (Correctly centered below images)
    input_frame = Frame(main_frame, bg='purple')

    Label(input_frame, text="Name :", font=("Arial", 14), bg='purple', fg='white').grid(row=0, column=0, padx=10, pady=5)
    name_entry = Entry(input_frame, font=("Arial", 14))
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_frame, text="Surname :", font=("Arial", 14), bg='purple', fg='white').grid(row=1, column=0, padx=10, pady=5)
    surname_entry = Entry(input_frame, font=("Arial", 14))
    surname_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(input_frame, text="Date of Birth :", font=("Arial", 14), bg='purple', fg='white').grid(row=2, column=0, padx=10, pady=5)
    dob_entry = Entry(input_frame, font=("Arial", 14))
    dob_entry.grid(row=2, column=1, padx=10, pady=5)

    input_frame.pack_forget()  

    # ✅ Start Button (Now correctly positioned below input fields when toggled)
    start_button = Button(main_frame, text="Start", font=("Arial", 14), bg='green', fg="white")
    start_button.pack_forget()  # Initially hidden

    root.mainloop()

create_ui()
