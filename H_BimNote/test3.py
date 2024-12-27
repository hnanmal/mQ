import tkinter as tk
import random

# Main application window
root = tk.Tk()
root.title("Simple 2D FPS Game")
root.geometry("800x600")

# Create a canvas
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

# Player and enemy setup
player = {"x": 400, "y": 550, "width": 10, "height": 20}
enemies = [
    {"x": random.randint(50, 750), "y": random.randint(50, 300)} for _ in range(5)
]
bullets = []


# Draw the player
def draw_player():
    canvas.create_rectangle(
        player["x"] - player["width"],
        player["y"] - player["height"],
        player["x"] + player["width"],
        player["y"] + player["height"],
        fill="blue",
    )


# Draw enemies
def draw_enemies():
    for enemy in enemies:
        canvas.create_oval(
            enemy["x"] - 10,
            enemy["y"] - 10,
            enemy["x"] + 10,
            enemy["y"] + 10,
            fill="red",
        )


# Draw bullets
def draw_bullets():
    for bullet in bullets:
        canvas.create_oval(
            bullet["x"] - 2,
            bullet["y"] - 5,
            bullet["x"] + 2,
            bullet["y"] + 5,
            fill="yellow",
        )


# Move bullets
def move_bullets():
    for bullet in bullets[:]:
        bullet["y"] -= 10
        if bullet["y"] < 0:
            bullets.remove(bullet)


# Collision detection
def check_collisions():
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (
                abs(bullet["x"] - enemy["x"]) < 10
                and abs(bullet["y"] - enemy["y"]) < 10
            ):
                bullets.remove(bullet)
                enemies.remove(enemy)


# Update the canvas
def update_canvas():
    canvas.delete("all")  # Clear the canvas
    draw_player()
    draw_enemies()
    draw_bullets()
    move_bullets()
    check_collisions()
    root.after(50, update_canvas)


# Key bindings for movement and shooting
def move_left(event):
    player["x"] -= 20


def move_right(event):
    player["x"] += 20


def shoot(event):
    bullets.append({"x": player["x"], "y": player["y"] - player["height"]})


# Bind keys
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", shoot)

# Start the game loop
update_canvas()
root.mainloop()
