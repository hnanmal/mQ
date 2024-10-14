# src/views/ui.py

import tkinter as tk
from PIL import Image, ImageTk  # Requires Pillow library to handle images
import time


def initialize_ui(root, state):
    pass


# Function to create the splash screen
def show_splash_screen():
    # Create a splash window
    splash = tk.Toplevel()
    splash.overrideredirect(True)  # Remove window decorations (title bar, close button)

    # Set the size and position of the splash screen
    splash.geometry("400x300+500+300")  # Set width, height, and position

    # Load the logo image (ensure the logo file is available)
    image = Image.open(
        "./resources/람쥐썬더.jpg"
    )  # Replace with the path to your logo image
    logo_image = ImageTk.PhotoImage(image)

    # Create a label to hold the image
    label = tk.Label(splash, image=logo_image)
    label.image = logo_image  # Keep a reference to avoid garbage collection
    label.pack()

    # # Show the splash screen for 3 seconds
    # splash.update()
    # time.sleep(1)  # Simulate loading time

    # # Destroy the splash screen after loading
    # splash.destroy()

    return splash  # Return the splash window object
