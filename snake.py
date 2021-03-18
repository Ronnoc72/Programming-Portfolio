from tkinter import *
from PIL import ImageTk, Image
import sys
import random


class Cons:
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27
    FONT = ('helvetica', 14)
    SMALL_FONT = ('helvetica', 8)


class Board(Canvas):
    def __init__(self):
        super(Board, self).__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT, background="black")
        self.init_game()
        self.pack()

    def init_game(self):
        """initializes game"""
        self.in_game = True
        self.dots = 3
        self.score = 0

        self.move_x = Cons.DOT_SIZE
        self.move_y = 0

        self.apple_x = 100
        self.apple_y = 190
        self.load_images()
        self.create_objects()
        # place the apple on the screen
        self.locate_apple()
        self.bind_all("<Key>", self.on_key_press)
        self.after(Cons.DELAY, self.on_timer)

    def load_images(self):
        """Loads the images of the game"""
        try:
            self.img_body = Image.open("images/body.png")
            self.img_head = Image.open("images/head.png")
            self.img_apple = Image.open("images/apple.png")
            self.body = ImageTk.PhotoImage(self.img_body)
            self.head = ImageTk.PhotoImage(self.img_head)
            self.apple = ImageTk.PhotoImage(self.img_apple)
        except IOError as e:
            print(e)
            sys.exit(1)

    def create_objects(self):
        """creates all the game objects that show on the screen"""
        self.create_text(30, 10, text=f"Score: {self.score}", tag="score", fill="white", font=Cons.SMALL_FONT)
        self.create_image(self.apple_x, self.apple_y, image=self.apple, anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(30, 50, image=self.body, anchor=NW, tag="body")
        self.create_image(40, 50, image=self.body, anchor=NW, tag="body")

    def locate_apple(self):
        """places a new apple on the screen"""
        apple = self.find_withtag("apple")
        self.delete(apple[0])
        ran_x = random.randint(0, Cons.MAX_RAND_POS)
        ran_y = random.randint(0, Cons.MAX_RAND_POS)
        self.apple_x = ran_x * Cons.DOT_SIZE
        self.apple_y = ran_y * Cons.DOT_SIZE
        self.create_image(self.apple_x, self.apple_y, anchor=NW, image=self.apple, tag="apple")

    def on_key_press(self, e):
        """deciding how to make the snake move"""
        key = e.keysym
        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.move_x <= 0:
            self.move_x = -Cons.DOT_SIZE
            self.move_y = 0
        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.move_x >= 0:
            self.move_x = Cons.DOT_SIZE
            self.move_y = 0
        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY and self.move_y <= 0:
            self.move_x = 0
            self.move_y = -Cons.DOT_SIZE
        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.move_y >= 0:
            self.move_x = 0
            self.move_y = Cons.DOT_SIZE

    def on_timer(self):
        """creates a game loop each timer event."""
        self.draw_score()
        self.check_collision()
        if self.in_game:
            self.apple_collision()
            self.move_snake()
            self.after(Cons.DELAY, self.on_timer)
        else:
            self.game_over()

    def draw_score(self):
        """Updates the score for the user"""
        score = self.find_withtag("score")
        self.itemconfigure(score, text=f"Score: {self.score}")

    def check_collision(self):
        """Checks for the collision from the user"""
        body_parts = self.find_withtag("body")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        over_lap = self.find_overlapping(x1, y1, x2, y2)

        for part in body_parts:
            for hit in over_lap:
                if hit == part:
                    self.in_game = False

        if x1 < 0:
            self.in_game = False
        elif x2 > Cons.BOARD_WIDTH:
            self.in_game = False
        elif y1 < 0:
            self.in_game = False
        elif y2 > Cons.BOARD_HEIGHT:
            self.in_game = False

    def apple_collision(self):
        """Checks the collisions with the apple and the snake position"""
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        over_lap = self.find_overlapping(x1, y1, x2, y2)
        for hit in over_lap:
            if hit == apple[0]:
                self.score += 1
                x, y = self.coords(hit)
                self.create_image(x, y, image=self.body, anchor=NW, tag="body")
                self.locate_apple()

    def move_snake(self):
        """Moves the snake object"""
        body_parts = self.find_withtag("body")
        head = self.find_withtag("head")
        snake = body_parts + head
        z = 0
        while z < len(snake) - 1:
            c1 = self.coords(snake[z])
            c2 = self.coords(snake[z + 1])
            self.move(snake[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1
        self.move(head, self.move_x, self.move_y)

    def game_over(self):
        """Displays the game over menu."""
        self.delete(ALL)
        self.create_text(Cons.BOARD_WIDTH / 2, Cons.BOARD_HEIGHT / 2, text="Game Over", fill="white", font=Cons.FONT)
        self.create_text(Cons.BOARD_WIDTH / 2, Cons.BOARD_HEIGHT / 1.75, text=f"Your Score was: {self.score}", fill="white", font=Cons.FONT)
        self.btn = Button(self, command=self.restart, text="Restart", font=Cons.SMALL_FONT)
        self.btn.place(x=Cons.BOARD_WIDTH / 2 - 20, y=Cons.BOARD_HEIGHT / 1.5)

    def restart(self):
        self.destroy()
        Snake(self.master)


class Snake(Frame):
    def __init__(self, master):
        super(Snake, self).__init__(master)
        self.master.title("Snake")
        self.board = Board()
        self.pack()


def main():
    root = Tk()
    snake = Snake(root)
    root.mainloop()


main()
