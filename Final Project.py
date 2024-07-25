'''
Author: Jesse Gore
Date: 7/15/2024
Assignment Project status report
Purpose: to create an ordering program that takes multiple selections, gives total price, delivery time, and driver or in-store pickup associate.
'''

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import random

# Constants
PIZZA_SIZES = {"Small": 5, "Medium": 8, "Large": 10}
TOPPINGS = {"Cheese": 1, "Pepperoni": 1, "Mushrooms": 1, "Onions": 1, "Bacon": 1}
MALE_NAMES = ["John", "Michael", "David", "James", "Robert"]
FEMALE_NAMES = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"]

MALE_IMAGES = [r"C:\Users\padri\OneDrive\Desktop\Final project\1.jpg", r"C:\Users\padri\OneDrive\Desktop\Final project\2.png"]
FEMALE_IMAGES = [r"C:\Users\padri\OneDrive\Desktop\Final project\3.jpg", r"C:\Users\padri\OneDrive\Desktop\Final project\4.jpg"]

IMAGE_PATH = r"C:\Users\padri\OneDrive\Desktop\Final project\pizza_palace.png"

class PizzaPalaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Palace")
        self.root.geometry("800x600")
        self.root.configure(bg="red")
        self.create_main_window()

    def create_main_window(self):
        self.clear_window()

        self.main_frame = tk.Frame(self.root, bg="red")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_label = tk.Label(self.main_frame, text="Welcome to Pizza Palace!", bg="red", fg="white")
        self.main_label.pack(pady=10)

        self.create_pizza_button = tk.Button(self.main_frame, text="Create Your Own Pizza", command=self.create_pizza_window, bg="white", fg="black")
        self.create_pizza_button.pack(pady=5)

        # Load and display the image
        try:
            self.image = Image.open(IMAGE_PATH)
            self.image = self.image.resize((400, 300), Image.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(self.main_frame, image=self.image, bg="red")
            self.image_label.pack(pady=10)
        except FileNotFoundError:
            print(f"Image not found: {IMAGE_PATH}")

    def create_pizza_window(self):
        self.clear_window()

        self.root.configure(bg="red")

        self.pizza_frame = tk.Frame(self.root, bg="red")
        self.pizza_frame.pack(fill=tk.BOTH, expand=True)

        self.pizza_label = tk.Label(self.pizza_frame, text="Create Your Own Pizza", bg="red", fg="white")
        self.pizza_label.pack(pady=10)

        self.size_label = tk.Label(self.pizza_frame, text="Choose Size:", bg="red", fg="white")
        self.size_label.pack()

        self.size_var = tk.StringVar(value=list(PIZZA_SIZES.keys())[0])
        for size, price in PIZZA_SIZES.items():
            frame = tk.Frame(self.pizza_frame, bg="red")
            frame.pack()

            canvas = tk.Canvas(frame, width=60, height=60, bg="red", highlightthickness=0)
            canvas.pack(side=tk.LEFT)

            if size == "Small":
                canvas.create_oval(15, 15, 45, 45, outline="black", fill="black")
            elif size == "Medium":
                canvas.create_oval(10, 10, 50, 50, outline="black", fill="black")
            elif size == "Large":
                canvas.create_oval(5, 5, 55, 55, outline="black", fill="black")

            rb = tk.Radiobutton(frame, text=f"{size} (${price})", variable=self.size_var, value=size, bg="red", fg="white", selectcolor="black")
            rb.pack(side=tk.LEFT)

        # Topping frame on the left
        self.topping_frame = tk.Frame(self.pizza_frame, bg="red")
        self.topping_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        self.topping_label = tk.Label(self.topping_frame, text="Choose Toppings:", bg="red", fg="white")
        self.topping_label.pack()

        self.topping_vars = []
        for topping, price in TOPPINGS.items():
            var = tk.BooleanVar()
            var.trace("w", self.update_pizza)
            frame = tk.Frame(self.topping_frame, bg="red")
            frame.pack(anchor='w')
            cb = tk.Checkbutton(frame, text=f"{topping} (${price})", variable=var, bg="red", fg="white", selectcolor="black")
            cb.pack(side=tk.LEFT)
            self.topping_vars.append((var, topping))

        self.quantity_label = tk.Label(self.topping_frame, text="Quantity:", bg="red", fg="white")
        self.quantity_label.pack()

        self.quantity_var = tk.StringVar(value="1")
        self.quantity_menu = tk.OptionMenu(self.topping_frame, self.quantity_var, *[str(i) for i in range(1, 21)])
        self.quantity_menu.config(bg="red", fg="white")
        self.quantity_menu.pack()

        self.back_button = tk.Button(self.pizza_frame, text="Back", command=self.create_main_window, bg="white", fg="black")
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(self.pizza_frame, text="Next", command=self.review_order, bg="white", fg="black")
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Generate and display the pizza with selected toppings
        self.generate_pizza()

    def generate_pizza(self):
        pizza_size = 200
        bg_size = pizza_size + 20

        self.pizza_canvas = tk.Canvas(self.pizza_frame, width=bg_size, height=bg_size, bg="red", highlightthickness=0)
        self.pizza_canvas.pack(pady=10)

        self.pizza_image = Image.new("RGBA", (pizza_size, pizza_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(self.pizza_image)

        # Draw pizza crust
        draw.ellipse((0, 0, pizza_size, pizza_size), fill="sandybrown", outline="sienna", width=5)

        # Draw pizza sauce
        draw.ellipse((20, 20, pizza_size-20, pizza_size-20), fill="tomato")

        self.pizza_image_tk = ImageTk.PhotoImage(self.pizza_image)
        self.pizza_canvas.create_image(bg_size//2, bg_size//2, image=self.pizza_image_tk)

    def update_pizza(self, *args):
        pizza_size = 200
        bg_size = pizza_size + 20

        self.pizza_image = Image.new("RGBA", (pizza_size, pizza_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(self.pizza_image)

        # Draw pizza crust
        draw.ellipse((0, 0, pizza_size, pizza_size), fill="sandybrown", outline="sienna", width=5)

        # Draw pizza sauce
        draw.ellipse((20, 20, pizza_size-20, pizza_size-20), fill="tomato")

        # Draw cheese
        draw.ellipse((30, 30, pizza_size-30, pizza_size-30), fill="yellow")

        # Draw selected toppings
        for var, topping in self.topping_vars:
            if var.get():
                self.draw_topping(draw, topping, pizza_size)

        self.pizza_image_tk = ImageTk.PhotoImage(self.pizza_image)
        self.pizza_canvas.create_image(bg_size//2, bg_size//2, image=self.pizza_image_tk)

    def draw_topping(self, draw, topping, pizza_size):
        if topping == "Pepperoni":
            for _ in range(10):
                x = random.randint(40, pizza_size - 60)
                y = random.randint(40, pizza_size - 60)
                draw.ellipse((x, y, x + 20, y + 20), fill="red", outline="darkred")
        elif topping == "Mushrooms":
            for _ in range(8):
                x = random.randint(40, pizza_size - 55)
                y = random.randint(40, pizza_size - 55)
                draw.rectangle((x, y, x + 15, y + 15), fill="tan", outline="saddlebrown")
        elif topping == "Onions":
            for _ in range(12):
                x = random.randint(40, pizza_size - 60)
                y = random.randint(40, pizza_size - 60)
                draw.arc((x, y, x + 20, y + 20), start=0, end=180, fill="purple")
        elif topping == "Bacon":
            for _ in range(8):
                x = random.randint(40, pizza_size - 60)
                y = random.randint(40, pizza_size - 60)
                draw.rectangle((x, y, x + 10, y + 30), fill="darkred", outline="black")

    def review_order(self):
        pizza_size = self.size_var.get()
        toppings = [topping for var, topping in self.topping_vars if var.get()]
        quantity = self.quantity_var.get()

        size_price = PIZZA_SIZES[pizza_size]
        toppings_price = sum([TOPPINGS[topping] for topping in toppings])
        total_price = int(quantity) * (size_price + toppings_price)

        self.clear_window()

        self.root.configure(bg="red")

        self.review_frame = tk.Frame(self.root, bg="red")
        self.review_frame.pack(fill=tk.BOTH, expand=True)

        order_summary = f"Order Summary:\n\nSize: {pizza_size} (${size_price})\n"
        order_summary += f"Toppings: {', '.join(toppings)} (${toppings_price})\n"
        order_summary += f"Quantity: {quantity}\nTotal Price: ${total_price}\n"

        self.order_summary_label = tk.Label(self.review_frame, text=order_summary, justify=tk.LEFT, bg="red", fg="white")
        self.order_summary_label.pack(pady=10)

        self.payment_button = tk.Button(self.review_frame, text="Proceed to Payment", command=self.payment_window, bg="white", fg="black")
        self.payment_button.pack(pady=5)

        self.back_button = tk.Button(self.review_frame, text="Back", command=self.create_pizza_window, bg="white", fg="black")
        self.back_button.pack(pady=5)

    def payment_window(self):
        self.clear_window()

        self.root.configure(bg="red")

        self.payment_frame = tk.Frame(self.root, bg="red")
        self.payment_frame.pack(fill=tk.BOTH, expand=True)

        self.payment_label = tk.Label(self.payment_frame, text="Payment/Delivery Options", bg="red", fg="white")
        self.payment_label.pack(pady=10)

        self.name_label = tk.Label(self.payment_frame, text="Name:", bg="red", fg="white")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.payment_frame)
        self.name_entry.pack()

        self.address_label = tk.Label(self.payment_frame, text="Address:", bg="red", fg="white")
        self.address_label.pack()
        self.address_entry = tk.Entry(self.payment_frame)
        self.address_entry.pack()

        self.delivery_label = tk.Label(self.payment_frame, text="Delivery or Pickup:", bg="red", fg="white")
        self.delivery_label.pack()

        self.delivery_var = tk.StringVar(value="Delivery")
        self.delivery_menu = tk.OptionMenu(self.payment_frame, self.delivery_var, "Delivery", "Pickup")
        self.delivery_menu.config(bg="red", fg="white")
        self.delivery_menu.pack()

        self.card_label = tk.Label(self.payment_frame, text="Credit Card Number:", bg="red", fg="white")
        self.card_label.pack()

        self.card_frame = tk.Frame(self.payment_frame, bg="red")
        self.card_frame.pack()

        self.card_entries = []
        for _ in range(4):
            entry = tk.Entry(self.card_frame, width=4, justify='center')
            entry.pack(side=tk.LEFT, padx=5)
            entry.bind("<KeyRelease>", self.card_entry_validation)
            self.card_entries.append(entry)

        self.expiration_label = tk.Label(self.payment_frame, text="Expiration Date (MM/YYYY):", bg="red", fg="white")
        self.expiration_label.pack()

        self.expiration_frame = tk.Frame(self.payment_frame, bg="red")
        self.expiration_frame.pack()

        self.expiration_month = tk.Entry(self.expiration_frame, width=2, justify='center')
        self.expiration_month.pack(side=tk.LEFT)
        tk.Label(self.expiration_frame, text="/", bg="red", fg="white").pack(side=tk.LEFT)
        self.expiration_year = tk.Entry(self.expiration_frame, width=4, justify='center')
        self.expiration_year.pack(side=tk.LEFT)

        self.cvv_label = tk.Label(self.payment_frame, text="CVV:", bg="red", fg="white")
        self.cvv_label.pack()

        self.cvv_entry = tk.Entry(self.payment_frame, width=3, justify='center')
        self.cvv_entry.pack()

        self.back_button = tk.Button(self.payment_frame, text="Back", command=self.review_order, bg="white", fg="black")
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.submit_button = tk.Button(self.payment_frame, text="Submit", command=self.submit_order, bg="white", fg="black")
        self.submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def card_entry_validation(self, event):
        widget = event.widget
        text = widget.get()
        if not text.isdigit() or len(text) > 4:
            widget.delete(4, tk.END)

        if len(text) == 4:
            current_index = self.card_entries.index(widget)
            if current_index < 3:
                self.card_entries[current_index + 1].focus()

    def submit_order(self):
        # Input validation
        if not self.name_entry.get() or not self.address_entry.get() or any(not entry.get() for entry in self.card_entries):
            messagebox.showerror("Error", "All fields are required!")
            return

        card_number = "".join(entry.get() for entry in self.card_entries)
        if not card_number.isdigit() or len(card_number) != 16:
            messagebox.showerror("Error", "Credit Card Number must be 16 digits long!")
            return

        expiration_month = self.expiration_month.get()
        expiration_year = self.expiration_year.get()
        if not expiration_month.isdigit() or not expiration_year.isdigit() or len(expiration_month) != 2 or len(expiration_year) != 4:
            messagebox.showerror("Error", "Expiration date must be in MM/YYYY format!")
            return

        cvv = self.cvv_entry.get()
        if not cvv.isdigit() or len(cvv) != 3:
            messagebox.showerror("Error", "CVV must be a 3-digit number!")
            return

        # Generate random order number and estimated time
        order_number = random.randint(1000, 9999)
        estimated_time = random.randint(20, 45)  # estimated time in minutes

        # Random driver or pickup name and image
        if self.delivery_var.get() == "Delivery":
            driver_name = random.choice(MALE_NAMES)
            delivery_message = f"Your order will be delivered by {driver_name}."
            image_path = random.choice(MALE_IMAGES)
        else:
            pickup_name = random.choice(FEMALE_NAMES)
            delivery_message = f"Your order will be ready for pickup by {pickup_name}."
            image_path = random.choice(FEMALE_IMAGES)

        # Display the order confirmation screen
        self.clear_window()
        confirmation_message = f"Order Confirmed!\n\nOrder Number: {order_number}\nEstimated Time: {estimated_time} minutes\n{delivery_message}"
        self.confirmation_label = tk.Label(self.root, text=confirmation_message, justify=tk.LEFT, bg="red", fg="white")
        self.confirmation_label.pack(pady=10)

        # Load and display the image
        try:
            self.delivery_image = Image.open(image_path)
            self.delivery_image = self.delivery_image.resize((200, 200), Image.LANCZOS)
            self.delivery_image = ImageTk.PhotoImage(self.delivery_image)
            self.delivery_image_label = tk.Label(self.root, image=self.delivery_image, bg="red")
            self.delivery_image_label.pack(pady=10)
        except FileNotFoundError:
            print(f"Image not found: {image_path}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaPalaceApp(root)
    root.mainloop()
