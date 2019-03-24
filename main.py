import piece
import piece_parser
import piece_drawer
import time
import random
import copy
import numpy as np
import math
from tkinter import *


def tick():
    global playing, main_canvas, placed_blocks, last_action, active_piece, piece_list, last_score, last_prisms, last_prisms_label, last_score_label, score, prisms

    if playing:

        main_canvas.after(30, tick)

        if time.time() > last_action + (3 * 0.9 ** level):  # The time taken for a piece to fall is based off the level.
            active_piece.offset[3] -= 1

            # If the piece is lowered and intersects with the blocks, the block has hit the ground.
            # Place the block and spawn a new one.
            if not active_piece.check_intersection(placed_blocks, grid_size):
                # Lock piece.
                active_piece.offset[3] += 1
                for piece in active_piece.get_moved_pieces():
                    placed_blocks.append(piece)
                check_cleared() # Clear any layers

                # Spawn new piece.
                # Add the extra_offset with (1,1,1,W-1) (W being the 4d height of the grid) to get the offset.
                active_piece = piece_list[random.randint(0, len(piece_list)-1)]
                for index in range(3):
                    active_piece.offset[index] = active_piece.extra_offset[index] + 1
                active_piece.offset[3] = active_piece.extra_offset[3] + grid_size[3] - 1

                # If, once a piece is spawned, it is already intersecting with the blocks,
                # initiate a game over and restart the board
                if not active_piece.check_intersection(placed_blocks, grid_size):
                    placed_blocks = []

                    last_score = score
                    score = 0
                    last_prisms = prisms
                    prisms = 0
                    last_score_label['text'] = "\nLast Score: {}".format(last_score)
                    last_prisms_label['text'] = "Last Prisms: {}".format(last_prisms)

            last_action = time.time()

        draw_frame()


def draw_frame():
    main_canvas.delete("all")

    piece_drawer.draw_grid(main_canvas, grid_size, placed_blocks, active_piece)


# Checks if any prisms have been cleared.
def check_cleared():
    global offset_level, placed_blocks, grid_size, score, prisms, score_label, prisms_label, level, level_label

    # Create a boolean array, set items to True if a block exists there.
    blocks_existing = np.zeros(grid_size[::-1])
    for piece in placed_blocks:
        if not piece[3] >= grid_size[3]:
            blocks_existing[piece[3]][piece[2]][piece[1]][piece[0]] = True

    # Append to cleared_layers the layer number if it has been cleared.
    cleared_layers = []
    for layer_num, layer in enumerate(blocks_existing):
        if 0 not in layer:
            cleared_layers.append(layer_num)

    # Update score, prisms, level
    score += (level+5) * 200 * len(cleared_layers) ** 2
    score_label['text'] = "Score: {}".format(score)

    prisms += len(cleared_layers)
    prisms_label['text'] = "Prisms: {}".format(prisms)

    level = offset_level + math.floor(prisms / 10)
    level_label = Label(root, text="Level {}".format(level))

    new_placed_blocks = placed_blocks[:]

    # Move any pieces above cleared layers down.
    for piece in placed_blocks:
        if piece[3] in cleared_layers:
            new_placed_blocks.remove(piece)
        else:
            go_down = 0

            for layer in cleared_layers:
                if piece[3] > layer:
                    go_down += 1

            piece[3] -= go_down

    placed_blocks = new_placed_blocks[:]


# Handles the key controls.
def control(event):
    global active_piece, placed_blocks, last_action, grid_size

    movement = {"w": (2,-1), "a": (0,-1), "s": (2,1), "d": (0,1), "q": (1,1), "e": (1,-1)}
    rotate = {"g": "XW", "h": "YW", "j": "ZW", "b": "XY", "n": "YZ", "m": "XZ"}
    key_pressed = str(event.char)

    if key_pressed in list(movement):
        movement_tuple = movement[key_pressed]
        test_piece = copy.deepcopy(active_piece)
        test_piece.offset[movement_tuple[0]] += movement_tuple[1]
        if test_piece.check_intersection(placed_blocks, grid_size):
            active_piece = test_piece

    elif key_pressed in list(rotate):
        test_piece = copy.deepcopy(active_piece)
        test_piece.rotate(rotate[key_pressed])
        if test_piece.check_intersection(placed_blocks, grid_size):
            active_piece = test_piece

    # Hard drop. Keep dropping the piece until it intersects,
    # and give a little bit of time for the player to move the piece before it locks in.
    elif key_pressed == " ":
        test_piece = copy.deepcopy(active_piece)
        while test_piece.check_intersection(placed_blocks, grid_size):
            test_piece.offset[3] -= 1
        test_piece.offset[3] += 1
        last_action = time.time() - 0.9 * (3 * 0.9 ** level)
        active_piece = test_piece


def load_initial_inputs():  # Load the start button, options, etc.
    global level_entry, grid_entry, playing, grid_size, offset_level

    Label(root, text="Level Start").pack()
    level_entry = Entry(root)
    if playing:
        level_entry.insert(0, str(offset_level))
    else:
        level_entry.insert(0, "0")
    level_entry.pack()

    Label(root, text="Grid Size").pack()
    grid_entry = Entry(root)
    if playing:
        grid_entry.insert(0, "x".join([str(coord) for coord in grid_size]))
    else:
        grid_entry.insert(0, "4x5x4x7")
    grid_entry.pack()

    start_button = Button(root, text="Start Game!", command=start_game)
    start_button.pack()


def start_game():
    global offset_level, grid_entry, level_entry, playing, main_canvas, score_label, level_label, last_prisms_label, last_score_label, prisms_label, grid_size, piece_list, active_piece, placed_blocks, last_action, score, prisms, last_score, last_prisms, level, root

    playing = True

    with open("pieces.txt") as f:
        piece_text = f.read().splitlines()

    grid_size = [int(coord) for coord in grid_entry.get().split("x")]

    piece_list = piece_parser.return_pieces(piece_text)

    active_piece = piece_list[random.randint(0, 3)]
    placed_blocks = []

    active_piece.offset = [1, 1, 1, grid_size[3] - 1]

    last_action = time.time()

    score = 0
    prisms = 0
    offset_level = int(level_entry.get())
    level = offset_level

    # Get rid of all remaining widgets and start packing new ones.
    for ele in root.winfo_children():
        ele.destroy()

    main_canvas = Canvas(root)
    piece_drawer.set_canvas_size(main_canvas, grid_size)
    main_canvas.pack()

    score_label = Label(root, text="Score: 0")
    score_label.pack()

    prisms_label = Label(root, text="Prisms: 0")
    prisms_label.pack()

    level_label = Label(root, text="Level {}".format(level))
    level_label.pack()

    last_score_label = Label(root, text="\nLast Score: {}".format(last_score))
    last_score_label.pack()

    last_prisms_label = Label(root, text="Last Prisms: {}".format(last_prisms))
    last_prisms_label.pack()

    load_initial_inputs()

    tick()


def kill():
    sys.exit()


root = Tk()
root.title("Tetris Plus")
root.bind("<Key>", control)

playing = False

last_score = 0
last_prisms = 0

load_initial_inputs()

while True:
    Tk().withdraw()

    root.protocol("WM_DELETE_WINDOW", kill)
    root.mainloop()
