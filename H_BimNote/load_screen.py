import os
import json
import textwrap
from tkinter import Tk, Frame, Button, Label, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Constants
THUMBNAIL_DIR = "thumbnails"
METADATA_FILE = "thumbnail_metadata.json"
THUMBNAIL_SIZE = (200, 200)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# Global variable to store recently loaded files
recent_files = []


def create_thumbnail(file_title, save_path, size=THUMBNAIL_SIZE):
    """
    Create a thumbnail with a background color derived from the file title.
    If the file title is too long, wrap it to fit within the thumbnail.
    """
    # Ensure thumbnail directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Generate color based on the file title
    color = generate_color_from_title(file_title)

    # Create an image
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)

    # Set up font (Double the font size)
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Adjust font size
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font

    # Calculate the maximum width for text wrapping
    max_width = size[0] - 10  # Leave some padding
    char_width = draw.textbbox((0, 0), "A", font=font)[2]
    wrap_width = max_width // char_width

    # Wrap the text to fit within the thumbnail
    wrapped_title = textwrap.fill(file_title, width=wrap_width)

    # Split wrapped text into lines
    lines = wrapped_title.split("\n")
    text_height = len(lines) * (font.getbbox("A")[3] - font.getbbox("A")[1])
    start_y = (size[1] - text_height) // 2.5

    # Draw each line of the wrapped text
    line_spacing_factor = 1.5

    for i, line in enumerate(lines):
        line_width = draw.textbbox((0, 0), line, font=font)[2]
        x_position = (size[0] - line_width) // 2
        y_position = start_y + i * int(
            (font.getbbox("A")[3] - font.getbbox("A")[1]) * line_spacing_factor
        )
        draw.text((x_position, y_position), line, fill=(255, 255, 255), font=font)

    # Save the thumbnail
    img.save(save_path)
    return save_path


def generate_color_from_title(title):
    """Generate a random color based on the hash of the title."""
    hash_value = sum(ord(char) for char in title)
    r = (hash_value * 123) % 256
    g = (hash_value * 321) % 256
    b = (hash_value * 231) % 256
    return (r, g, b)


def save_metadata(metadata):
    """Save metadata to a JSON file."""
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)


def load_metadata():
    """Load metadata from a JSON file."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def add_file_to_metadata(file_title, thumbnail_path):
    """Add file metadata and save."""
    metadata = load_metadata()
    metadata[file_title] = thumbnail_path
    save_metadata(metadata)


def create_and_store_thumbnail(file_title):
    """Create a thumbnail for a file and store its metadata."""
    thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{file_title}.png")
    create_thumbnail(file_title, thumbnail_path)
    add_file_to_metadata(file_title, thumbnail_path)


def display_thumbnails():
    """Display thumbnails from saved metadata."""
    metadata = load_metadata()
    for file_title, thumbnail_path in metadata.items():
        print(f"Thumbnail for '{file_title}': {thumbnail_path}")
        # Replace this print statement with GUI code to render thumbnails
        # For example, load the thumbnail image and display it in a GUI


def load_db_file():
    """
    Load a `.bnote` file and add it to the recent files list.
    """
    file_path = filedialog.askopenfilename(
        title="Open .bnote file", filetypes=[("bnote files", "*.bnote")]
    )
    if not file_path:
        return

    # Add the file to the recent files list
    file_name = os.path.basename(file_path)
    recent_files.append(file_path)

    # Generate thumbnail
    thumbnail_path = os.path.join(THUMBNAIL_DIR, file_name + ".png")
    create_thumbnail(file_name, thumbnail_path)

    # Refresh the thumbnails
    refresh_recent_files()


def refresh_recent_files():
    """
    Refresh the display of recently loaded files with thumbnails.
    """
    for widget in thumbnail_frame.winfo_children():
        widget.destroy()

    for file_path in recent_files:
        file_name = os.path.basename(file_path)
        thumbnail_path = os.path.join(THUMBNAIL_DIR, file_name + ".png")

        # Load the thumbnail image
        try:
            img = Image.open(thumbnail_path)
            img.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading thumbnail for {file_name}: {e}")
            continue

        # Create a thumbnail button
        button = Button(
            thumbnail_frame, image=photo, command=lambda fp=file_path: open_file(fp)
        )
        button.image = photo  # Keep a reference to avoid garbage collection
        button.pack(side="left", padx=10, pady=10)


def open_file(file_path):
    """
    Simulate opening the `.bnote` file.
    """
    print(f"Opening file: {file_path}")


# Module execution section
if __name__ == "__main__":
    # Create the main application window
    root = Tk()
    root.title("Recently Loaded DB Files")
    root.geometry("800x600")

    # Main frame
    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Load DB file button
    load_button = Button(main_frame, text="Load .bnote File", command=load_db_file)
    load_button.pack(pady=20)

    # Thumbnails frame
    thumbnail_frame = Frame(main_frame)
    thumbnail_frame.pack(fill="both", expand=True)

    load_metadata()
    # Start the application
    root.mainloop()
