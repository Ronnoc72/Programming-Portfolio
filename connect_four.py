from tkinter import *
from tkinter.font import families

HEIGHT = 500
WIDTH = 550
TITLE = "Connect Four"
BACKGROUND = "gray88"
FONT = ("SimSun", 24)
SMALL_FONT = ("SimSun", 12)
# main board that changes from the user's decisions.
board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]


class Piece(object):
    """Connect Four piece that stores the data for the grid and physical position."""
    def __init__(self, x, color, grid_x):
        self.x = x + 5
        self.y = self.grid_y = 0
        self.color = color
        self.grid_x = grid_x

    def calc_y(self, current_turn):
        """calculates the y position and for grid"""
        for i in reversed(range(len(board))):
            if board[i][self.grid_x] == 0:
                if current_turn:
                    board[i][self.grid_x] = 1
                else:
                    board[i][self.grid_x] = 2
                self.grid_y = i
                self.y = (i * 50) + 10
                break


class App(Frame):
    """Main game"""
    def __init__(self, master):
        super(App, self).__init__(master)
        self.current_turn = True
        self.current_color = "red"
        self.pieces = []
        self.canvas = Canvas(width=400, height=400)
        self.hover_canvas = Canvas(width=400, height=50, background="gray88")
        self.pack()
        self.create_widgets()
        self.canvas.place(x=75, y=50)
        self.hover_canvas.place(x=75, y=0)
        Button(bg="cornflowerblue", command=self.reset, text="Reset", font=SMALL_FONT, border=0).pack(side=BOTTOM)
        Button(bg="cornflowerblue", command=quit, text="Quit", font=SMALL_FONT, border=0).pack(side=BOTTOM)
        self.lbl = Label(bg="gray88", font=FONT)
        self.lbl.pack()

    def create_widgets(self):
        """makes all of the physical elements on the page"""
        self.canvas.create_rectangle(0, 0, 425, 400, fill="yellow", outline="gray50", width=3)
        for x in range(8):
            for y in range(8):
                self.canvas.create_oval((x * 50) + 5, (y * 50) + 5, (x * 50) + 45, (y * 50) + 45, fill="gray25",
                                        width=0)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_motion)

    def reset(self):
        """clears the board and pieces array to play another match"""
        self.canvas.unbind("<Button-1>")
        self.canvas.delete(ALL)
        self.create_widgets()
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] != 0:
                    board[x][y] = 0
        self.pieces.clear()
        self.lbl["text"] = ""

    def handle_click(self, e):
        """gets the mouse position and updates the board accordingly"""
        key = e.x
        self.update_board(5, 0) if 5 < key < 50 else None
        self.update_board(55, 1) if 55 < key < 100 else None
        self.update_board(105, 2) if 105 < key < 150 else None
        self.update_board(155, 3) if 155 < key < 200 else None
        self.update_board(205, 4) if 205 < key < 250 else None
        self.update_board(255, 5) if 255 < key < 300 else None
        self.update_board(305, 6) if 305 < key < 350 else None
        self.update_board(355, 7) if 355 < key < 400 else None
        self.display_board()
        if not self.current_turn:
            self.check_win(1)
        else:
            self.check_win(2)

    def handle_motion(self, e):
        """gets the mouse position and updates the display piece accordingly"""
        key = e.x
        self.display_piece(0) if 5 < key < 50 else None
        self.display_piece(50) if 55 < key < 100 else None
        self.display_piece(100) if 105 < key < 150 else None
        self.display_piece(150) if 155 < key < 200 else None
        self.display_piece(200) if 205 < key < 250 else None
        self.display_piece(250) if 255 < key < 300 else None
        self.display_piece(300) if 305 < key < 350 else None
        self.display_piece(350) if 355 < key < 400 else None

    def display_board(self):
        """displays the pieces on the canvas by getting the attributes of the piece object"""
        for piece in self.pieces:
            self.canvas.create_oval(piece.x, piece.y, piece.x + 30, piece.y + 30, fill=piece.color)

    def update_board(self, pos, index):
        """updates the pieces array and changes the current color and turn."""
        piece = Piece(pos, self.current_color, index)
        piece.calc_y(self.current_turn)
        self.pieces.append(piece)
        self.current_turn = not self.current_turn
        if self.current_color == "red":
            self.current_color = "blue"
        else:
            self.current_color = "red"

    def display_piece(self, x):
        """displays the piece that displays when the user hovers over a section."""
        self.hover_canvas.delete(ALL)
        self.hover_canvas.create_oval(x + 5, 5, x + 45, 45, fill=self.current_color, width=0)

    def update_win(self):
        """only called when a check_win condition is correct and gets the according message to display"""
        if self.current_turn:
            self.lbl["text"] = "Blue Wins"
            self.canvas.unbind("<Button-1>")
        else:
            self.lbl["text"] = "Red Wins"
            self.canvas.unbind("<Button-1>")

    def check_win(self, index):
        """main logic for checking the win"""
        for x in range(len(board) - 3):
            for y in range(len(board[x])):
                if board[x][y] == board[x + 1][y] == board[x + 2][y] == board[x + 3][y] == index:
                    self.update_win()
        for x in range(len(board)):
            for y in range(len(board[x]) - 3):
                if board[x][y] == board[x][y + 1] == board[x][y + 2] == board[x][y + 3] == index:
                    self.update_win()
        for x in range(len(board) - 3):
            for y in range(len(board[x]) - 3):
                if board[x][y] == board[x + 1][y + 1] == board[x + 2][y + 2] == board[x + 3][y + 3] == index:
                    self.update_win()
        for x in range(len(board) - 3):
            for y in range(len(board[x])):
                if board[x][y] == board[x + 1][y - 1] == board[x + 2][y - 2] == board[x + 3][y - 3] == index:
                    self.update_win()


def main():
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title(TITLE)
    root.config(bg=BACKGROUND)
    root.resizable(False, False)
    App(root)
    # getting the fonts available in tkinter
    # for family in families():
    #     print(family)
    root.mainloop()


main()
