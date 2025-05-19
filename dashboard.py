import random
import string
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageSequence
from tkinter import filedialog, messagebox
from fuzzywuzzy import process
import cv2
import numpy as np
import numpy as np
import boto3
import random

# Define the categories for quiz generation
categories = {
    "Animals": ["Cattle", "Cow", "Livestock", "Mammal", "Dairy Cow", "Dog", "Cat", "Elephant", "Tiger", "Cow", "Cattle", "Livestock", "Mammal"],
    "Fruits": ["Apple", "Banana", "Grapes", "Orange"],
    "House Items": ["Chair", "Lamp", "Table", "Clock"],
    "Shapes": ["Circle", "Square", "Triangle", "Rectangle"]
}


def find_closest_match(detected_label):
    detected_label_lower = detected_label.lower()
    best_match = None
    highest_score = 0

    for category, items in categories.items():
        for item in items:
            match_score = process.extractOne(detected_label_lower, items)[1]
            if match_score > highest_score:
                highest_score = match_score
                best_match = item

    # Only accept high-confidence matches
    return best_match if highest_score > 80 else None


class DashboardApp:
    def __init__(self, root, participant_name="ToonMaster"):
        self.root = root
        self.root.title("Toony Brain - Dashboard")
        self.root.geometry("1000x600")
        self.root.configure(bg="#8000ff")  # Purple background

        self.participant_name = participant_name
        self.sidebar_visible = False
        self.selected_category = None
        self.category_buttons = {}
        self.category_images = {}

        # This will store path of uploaded image
        self.img_path = None

        # Define categories as an instance variable
        self.categories = {
            "Animals": ["Dog", "Cat", "Elephant", "Tiger", "Cow"],
            "Fruits": ["Apple", "Banana", "Grapes", "Orange"],
            "House Items": ["Chair", "Lamp", "Table", "Clock"],
            "Shapes": ["Circle", "Square", "Triangle", "Rectangle"]
        }

        # Add horizontal line under categories
        line = tk.Frame(self.root, bg="grey", height=2, width=1200)
        line.place(relx=0.5, y=400, anchor="n")

        self.setup_ui()

    def setup_ui(self):
        # Load and display animated GIF (replacing heading)
        try:
            self.toonify_frames = [ImageTk.PhotoImage(img.copy().convert("RGBA"))
                                   for img in ImageSequence.Iterator(Image.open("assets/toonify.gif"))]
            self.toonify_label = tk.Label(self.root, bg="#8000ff")
            self.toonify_label.place(relx=0.5, y=10, anchor="n")
            self.animate_gif(0)
        except Exception as e:
            print("Error loading GIF:", e)

        # Hamburger Menu
        try:
            menu_img = Image.open(
                "assets/b-menu.png").resize((70, 50), Image.Resampling.LANCZOS)
            self.menu_icon = ImageTk.PhotoImage(menu_img)
            self.menu_button = tk.Button(self.root, image=self.menu_icon, bg="#8000ff",
                                         bd=0, activebackground="#8000ff", command=self.toggle_sidebar)
            self.menu_button.place(x=20, y=5)
        except Exception as e:
            print("Error loading menu icon:", e)

        # Sidebar Frame
        self.sidebar = tk.Frame(self.root, bg="#87e800", width=300, height=900)
        try:
            close_img = Image.open(
                "assets/side-menu.png").resize((70, 50), Image.Resampling.LANCZOS)
            self.close_icon = ImageTk.PhotoImage(close_img)
            self.close_btn = tk.Button(self.sidebar, image=self.close_icon, command=self.toggle_sidebar,
                                       bg="#87e800", bd=0, activebackground="#87e800", cursor="hand2")
            self.close_btn.place(x=220, y=10)
        except Exception as e:
            print("Error loading close icon:", e)

        # Profile Heading
        profile_label = tk.Label(self.sidebar, text="Profile", font=(
            "Arial", 16, "bold"), bg="#87e800", fg="black")
        profile_label.place(x=20, y=70)

        # Horizontal Line
        line = tk.Frame(self.sidebar, bg="black", height=2, width=260)
        line.place(x=20, y=100)

        # Profile Fields with improved spacing
        tk.Label(self.sidebar, text="Name:", font=("Arial", 12),
                 bg="#87e800", anchor="w").place(x=20, y=110)
        tk.Label(self.sidebar, text="Banzi", font=("Arial", 12, "bold"),
                 bg="#87e800", anchor="w").place(x=100, y=110)

        tk.Label(self.sidebar, text="Surname:", font=("Arial", 12),
                 bg="#87e800", anchor="w").place(x=20, y=150)
        tk.Label(self.sidebar, text="Dube", font=("Arial", 12, "bold"),
                 bg="#87e800", anchor="w").place(x=100, y=150)

        tk.Label(self.sidebar, text="Level:", font=("Arial", 12),
                 bg="#87e800", anchor="w").place(x=20, y=190)
        self.level_label = tk.Label(self.sidebar, text="Beginner", font=(
            "Arial", 12, "bold"), bg="#87e800", anchor="w")
        self.level_label.place(x=100, y=190)

        tk.Label(self.sidebar, text="Highest Score:", font=(
            "Arial", 12), bg="#87e800", anchor="w").place(x=20, y=230)
        self.score_label = tk.Label(self.sidebar, text="0", font=(
            "Arial", 12, "bold"), bg="#87e800", anchor="w")
        self.score_label.place(x=140, y=230)

        # Add cup icon to the right of "Highest Score"
        try:
            cup_img = Image.open(
                "assets/cup.png").resize((24, 24), Image.Resampling.LANCZOS)
            self.cup_icon = ImageTk.PhotoImage(cup_img)
            cup_label = tk.Label(
                self.sidebar, image=self.cup_icon, bg="#87e800")
            cup_label.place(x=220, y=228)  # Slight vertical alignment tweak
        except Exception as e:
            print("Error loading cup icon:", e)

        # Category frame
        self.category_frame = tk.Frame(self.root, bg="#8000ff")
        self.category_frame.place(relx=0.5, y=250, anchor="n")

        categories = {
            "Animals": "animals.jpg",
            "Food": "fruities.jpg",
            "House Items": "house-items.jpg",
            "Shapes": "shapes.png"
        }

        for idx, (name, file) in enumerate(categories.items()):
            normal_img = self.load_rounded_image(
                f"assets/{file}", (120, 120), 20, highlight=False)
            highlighted_img = self.load_rounded_image(
                f"assets/{file}", (120, 120), 20, highlight=True)

            button = tk.Label(self.category_frame, image=normal_img, bd=0,
                              relief="flat", bg="#8000ff", cursor="hand2")
            button.image = normal_img
            button.grid(row=0, column=idx, padx=20, pady=10)
            button.bind("<Button-1>", lambda e, cat=name,
                        b=button: self.select_category(cat, b))

            self.category_buttons[name] = button
            self.category_images[name] = {
                "normal": normal_img,
                "highlighted": highlighted_img
            }

    def load_rounded_image(self, path, size, radius, highlight=False):
        img = Image.open(path).resize(
            size, Image.Resampling.LANCZOS).convert("RGBA")
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + size, radius=radius, fill=255)

        rounded_img = Image.new('RGBA', size)
        rounded_img.paste(img, (0, 0), mask)

        if not highlight:
            return ImageTk.PhotoImage(rounded_img)
        else:
            border_size = 6
            bordered_size = (size[0] + border_size * 2,
                             size[1] + border_size * 2)
            bordered = Image.new('RGBA', bordered_size, (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(bordered)
            border_draw.rounded_rectangle(
                (0, 0) + bordered_size, radius=radius + border_size, outline="lime", width=4)
            bordered.paste(rounded_img, (border_size,
                           border_size), rounded_img)

            try:
                tick = Image.open(
                    "assets/tick.png").resize((30, 30), Image.Resampling.LANCZOS)
                bordered.paste(tick, (bordered_size[0] - 35, 5), tick)
            except Exception as e:
                print("Error loading tick icon:", e)

            return ImageTk.PhotoImage(bordered)

    def select_category(self, name, widget):
        if self.selected_category == name:
            widget.configure(image=self.category_images[name]["normal"])
            widget.image = self.category_images[name]["normal"]
            self.selected_category = None
        else:
            if self.selected_category:
                prev_button = self.category_buttons[self.selected_category]
                prev_button.configure(
                    image=self.category_images[self.selected_category]["normal"])
                prev_button.image = self.category_images[self.selected_category]["normal"]

            widget.configure(image=self.category_images[name]["highlighted"])
            widget.image = self.category_images[name]["highlighted"]
            self.selected_category = name
            self.root.after(300, self.show_cartoonify_screen)

    def animate_gif(self, frame_index):
        frame = self.toonify_frames[frame_index]
        self.toonify_label.configure(image=frame)
        self.root.after(100, self.animate_gif, (frame_index + 1) %
                        len(self.toonify_frames))

    def show_cartoonify_screen(self):
        self.category_frame.place_forget()
        self.cartoonify_frame = tk.Frame(self.root, bg="#8000ff")
        self.cartoonify_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Upload and Cartoonify Buttons
        button_frame = tk.Frame(self.cartoonify_frame, bg="#8000ff")
        button_frame.pack(pady=15)

        upload_btn = tk.Button(button_frame, text="Upload Image",
                               command=self.upload_image, bg="white", fg="black")
        upload_btn.pack(side="left", padx=10)

        cartoonify_btn = tk.Button(button_frame, text="Cartoonify Image",
                                   command=self.cartoonify_image, bg="white", fg="black")
        cartoonify_btn.pack(side="left", padx=10)

        self.save_btn = tk.Button(button_frame, text="Save Cartoon",
                                  command=self.save_image, bg="white", fg="black", state="disabled")
        self.save_btn.pack(side="left", padx=10)

        back_btn = tk.Button(button_frame, text="Back to Categories",
                             command=self.back_to_dashboard, bg="white", fg="black")
        back_btn.pack(side="left", padx=10)

        # Frame for original and cartoon images
        self.images_frame = tk.Frame(self.cartoonify_frame, bg="#8000ff")
        self.images_frame.pack(pady=10)

        # Label for showing original image preview
        self.preview_label = tk.Label(self.images_frame, bg="#8000ff")
        self.preview_label.pack(side="left", expand=True, padx=20)

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.img_path = file_path
            labels = self.detect_labels(file_path)
            # Generate quiz based on first detected label
            self.generate_quiz(labels[0])

            try:
                # Convert to RGB for PIL preview
                self.original_cv_img = cv2.imread(file_path)
                img_rgb = cv2.cvtColor(self.original_cv_img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)
                pil_img = pil_img.resize((200, 200), Image.Resampling.LANCZOS)
                self.preview_img_tk = ImageTk.PhotoImage(pil_img)
                self.preview_label.configure(image=self.preview_img_tk)
                self.save_btn.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

            labels = self.detect_labels(file_path)
            print("Detected Labels:", labels)  # Check detected objects

    def apply_cartoon_effect(self, img):
        # Cartoonify effect using OpenCV
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

        color = cv2.bilateralFilter(img, 9, 250, 250)

        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    def cartoonify_image(self):
        if not hasattr(self, "original_cv_img"):
            messagebox.showwarning(
                "Warning", "Please upload an image before cartoonifying.")
            return

        cartoon = self.apply_cartoon_effect(self.original_cv_img)
        cartoon_resized = cv2.resize(cartoon, (200, 200))
        cartoon_rgb = cv2.cvtColor(cartoon_resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cartoon_rgb)
        self.cartoon_img = img
        self.cartoon_img_tk = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=self.cartoon_img_tk)
        self.save_btn.config(state="normal")

    def save_image(self):
        if hasattr(self, "cartoon_img"):
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files",
                                                                 "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                try:
                    self.cartoon_img.save(file_path)
                    messagebox.showinfo(
                        "Saved", "Cartoon image saved successfully.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Failed to save image:\n{e}")
        else:
            messagebox.showwarning("Warning", "No cartoon image to save.")

    def back_to_dashboard(self):
        if hasattr(self, "cartoonify_frame"):
            self.cartoonify_frame.place_forget()
        self.category_frame.place(relx=0.5, y=250, anchor="n")

    def detect_labels(self, image_path):
        client = boto3.client('rekognition')

        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            response = client.detect_labels(
                Image={'Bytes': image_bytes},
                MaxLabels=5,
                MinConfidence=70
            )
            labels = [label['Name'] for label in response['Labels']]
            return labels

    def generate_quiz(self, detected_label):
        detected_label_lower = detected_label.lower()

        for category, items in categories.items():
            items_lower = [item.lower() for item in items]
            if detected_label_lower in items_lower:
                correct_answer = detected_label
                wrong_answers = random.sample(
                    [item for item in items if item.lower(
                    ) != correct_answer.lower()], min(3, len(items)-1)
                )
                options = wrong_answers + [correct_answer]
                random.shuffle(options)

                question = f"Which of the following is a {category}?"
                self.display_quiz(question, options, correct_answer)
                return

        messagebox.showinfo(
            "Quiz Info", f"'{detected_label}' not found in predefined categories. Try another image!")

    def display_quiz(self, question, options, correct_answer):
        quiz_frame = tk.Frame(self.root, bg="#8000ff")
        # Lowered placement
        quiz_frame.place(relx=0.5, rely=0.7, anchor="center")

        tk.Label(quiz_frame, text=question, font=("Arial", 16, "bold"),
                 bg="#8000ff", fg="white").pack(pady=10)

        btn_frame = tk.Frame(quiz_frame, bg="#8000ff")  # Holds answer buttons
        btn_frame.pack(pady=5)

        # Create answer buttons in two rows
        btn_colors = "#32CD32"  # Green color for answers
        btn_width = 12

        for i, option in enumerate(options):
            btn = tk.Button(btn_frame, text=option, font=("Arial", 14), bg=btn_colors, fg="white",
                            width=btn_width, height=2, command=lambda o=option: self.check_answer(o, correct_answer))

            if i < 2:
                btn.grid(row=0, column=i, padx=10, pady=5)  # First row: A & B
            else:
                btn.grid(row=1, column=i-2, padx=10,
                         pady=5)  # Second row: C & D

        self.participant_scores = []  # Initialize score tracking

    def check_answer(self, chosen_option, correct_answer):
        self.participant_scores.append(
            1 if chosen_option == correct_answer else 0)
        accuracy = np.mean(self.participant_scores) * 100
        messagebox.showinfo(
            "Quiz Result", f"Your accuracy so far: {accuracy:.2f}%")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.place_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.place(x=0, y=0)
            self.sidebar_visible = True


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
