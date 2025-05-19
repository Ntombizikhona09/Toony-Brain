import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import pyttsx3

class CartoonifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Toony Brain - Cartoonify Your Picture!")
        self.root.geometry("900x650")
        self.root.configure(bg="#FFF8DC")

        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        self.original_image = None
        self.cartoon_image = None

        self.title_font = ("Comic Sans MS", 28, "bold")
        self.button_font = ("Comic Sans MS", 14, "bold")
        self.text_font = ("Comic Sans MS", 16)

        self.setup_gui()

    def speak(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    def setup_gui(self):
        # NAVIGATION BAR
        nav_bar = tk.Frame(self.root, bg="#ff6f61", height=60)
        nav_bar.pack(fill="x")
        title_label = tk.Label(nav_bar, text="🎨 Toony Brain", font=("Comic Sans MS", 22, "bold"), fg="white", bg="#ff6f61")
        title_label.pack(pady=10)

        # SIDEBAR MENU (STYLE OPTIONS)
        sidebar = tk.Frame(self.root, bg="#6a9ae2", width=200)
        sidebar.pack(side="left", fill="y")

        style_label = tk.Label(sidebar, text="Choose Style:", font=("Comic Sans MS", 16), fg="white", bg="#6a9ae2")
        style_label.pack(pady=10)

        self.cartoon_styles = ttk.Combobox(sidebar, values=["Classic Sketch", "Bold Lines", "Watercolor", "Soft Glow"])
        self.cartoon_styles.pack(pady=5)

        # MASCOT MESSAGE
        self.mascot_message = tk.Label(
            self.root,
            text="Hi! Let's make your photo into a fun cartoon! 🐱\nStep 1: Click 📷 Open Picture.",
            font=self.text_font,
            bg="#FFF8DC",
            fg="#333333",
            justify="center",
            wraplength=500
        )
        self.mascot_message.pack(pady=10)
        self.speak("Hi! Let's make your photo into a fun cartoon! Step one: click open picture.")

        # BUTTON FRAME
        button_frame = tk.Frame(self.root, bg="#FFF8DC")
        button_frame.pack(pady=10)

        open_btn = tk.Button(button_frame, text="📷 Open Picture", font=self.button_font, command=self.open_image, bg="#ff6f61", fg="white", relief="raised", bd=3)
        open_btn.grid(row=0, column=0, padx=10)

        cartoonify_btn = tk.Button(button_frame, text="✨ Cartoonify!", font=self.button_font, command=self.cartoonify, bg="#6a9ae2", fg="white", relief="raised", bd=3)



        cartoonify_btn.grid(row=0, column=1, padx=10)

        save_btn = tk.Button(button_frame, text="💾 Save Cartoon", font=self.button_font, command=self.save_image, bg="#34a853", fg="white", relief="raised", bd=3)
        save_btn.grid(row=0, column=2, padx=10)

        # Apply hover effects to buttons
        for btn in [open_btn, cartoonify_btn, save_btn]:
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#444"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#ff6f61" if e.widget == open_btn else "#6a9ae2"))

        # IMAGE DISPLAY CANVAS
        self.image_canvas = tk.Canvas(self.root, width=700, height=450, bg="#fff")
        self.image_canvas.pack(pady=15)

    def update_mascot_message(self, message):
        self.mascot_message.config(text=message)
        self.speak(message)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            self.update_mascot_message("Oops! You didn't select any picture. Try again! 📷")
            return

        self.original_image = cv2.imread(file_path)
        if self.original_image is None:
            self.update_mascot_message("Failed to load the image. Try a different one!")
            return

        self.display_image(self.original_image)
        self.update_mascot_message("Great! Now click cartoonify to see the magic!")

        def cartoonify_image(self):
            if self.original_image is None:
                messagebox.showwarning("Hey!", "Please open a picture first! 📷")
                self.speak("Please open a picture first!")
                return
            
            # Convert image to grayscale
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            
            # Apply Median Blur
            gray = cv2.medianBlur(gray, 5)

            # Detect edges using Adaptive Thresholding
            edges = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                blockSize=9,
                C=9
            )

            # Apply bilateral filtering for a smoother effect
            color = cv2.bilateralFilter(self.original_image, d=9, sigmaColor=300, sigmaSpace=300)

            # Sharpen edges further for stronger contrast
            cartoon = cv2.bitwise_and(color, color, mask=edges)

            # Apply a stylization filter to enhance the cartoon effect
            cartoon = cv2.stylization(self.original_image, sigma_s=150, sigma_r=0.25)

            # Store cartoon image
            self.cartoon_image = cartoon
            self.display_image(cartoon)

            self.update_mascot_message("Look! Your cartoon is ready! 💫 You can save it now!")



    def save_image(self):
        if self.cartoon_image is None:
            messagebox.showinfo("Oops!", "No cartoon image to save. Make one first! 🖌")
            self.speak("No cartoon image to save. Make one first!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
        )
        if file_path:
            cv2.imwrite(file_path, self.cartoon_image)
            messagebox.showinfo("Yay!", "Your cartoon picture is saved! 🎉")
            self.update_mascot_message("Awesome! You saved your cartoon! Want to try another?")

    def display_image(self, img):
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            pil_img = pil_img.resize((700, 450), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(pil_img)

            self.image_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
            self.image_canvas.image = self.img_tk  # Prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Could not display image: {e}")
            self.speak("Something went wrong displaying the image.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CartoonifyApp(root)
    root.mainloop()
