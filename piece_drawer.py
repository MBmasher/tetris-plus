import colorsys
import piece
from tkinter import *

size_difference_base = 25
size_difference      = 3


# Base the piece colour based on its height in the z axis.
# This makes 3D visualisation a lot easier
def get_piece_colour(height, layer_height):
    rgb_tuple = colorsys.hsv_to_rgb(height/layer_height, 1, 1)
    int256_tuple = tuple([min(int(colour * 256), 255) for colour in rgb_tuple])

    return '#%02x%02x%02x' % int256_tuple


def draw_grid(canvas, grid_size, placed_blocks, active_piece):
    centre_start = [((grid_size[0] / 2) * (size_difference_base + size_difference * grid_size[1])),
                    ((grid_size[2] / 2) * (size_difference_base + size_difference * grid_size[1]))]
    layer_distance = ((grid_size[0]) * (size_difference_base + size_difference * grid_size[1])) + 20

    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            for z in range(grid_size[2]):
                for w in range(grid_size[3]):
                    square_fill    = None
                    square_outline = "#aaaaaa"
                    square_width   = 0.5+(y/4)

                    # If a piece is not active and already placed, change the fill and offset
                    if [x,y,z,w] in placed_blocks or [x,y,z,w] in active_piece.get_moved_pieces():
                        square_fill = get_piece_colour(y, grid_size[1])

                        if [x,y,z,w] in active_piece.get_moved_pieces():
                            square_outline = "#000000"
                            square_width = 2+(y/2)

                    # Lots of math to determine the drawing position.
                    centre_draw    = [centre_start[0] + w*layer_distance, centre_start[1]]
                    centre_squares = [grid_size[0]/2, grid_size[2]/2]

                    size     = size_difference_base + size_difference*y
                    x_offset = centre_draw[0] + (x-centre_squares[0])*size
                    z_offset = centre_draw[1] + (z-centre_squares[1])*size

                    canvas.create_rectangle(x_offset, z_offset, x_offset + size, z_offset + size,
                                            fill=square_fill, outline=square_outline, width = square_width)


def set_canvas_size(canvas, grid_size):
    x_size = (grid_size[0]) * (size_difference_base + size_difference * grid_size[1])
    z_size = (grid_size[2]) * (size_difference_base + size_difference * grid_size[1])

    canvas_width = grid_size[3] * (x_size + 20)
    canvas_height = z_size

    canvas.config(width=canvas_width, height=canvas_height)