class Piece:

    def __init__(self, id, centre, pieces, offset, extra_offset):
        self.id = id
        self.centre = centre
        self.pieces = pieces
        self.offset = offset
        self.extra_offset = extra_offset

    # in 4D, each piece rotates along 2 axes. example: a XY rotation will change the Z and W coordinates of the piece
    def rotate(self, axis):
        axes = {"X": 0, "Y": 1, "Z": 2, "W": 3}
        used_axes = [axes[index] for index in axis]
        rotation_axis1, rotation_axis2 = [axis_num for axis_num in range(4) if axis_num not in used_axes]

        new_pieces = []
        for piece in self.pieces:
            new_piece = [0, 0, 0, 0]
            for index in range(4):
                # Among the two coordinates that are changing, here is how they are changed:
                # (coord1, coord2) -> (coord2, -coord1)
                if index == rotation_axis1:
                    new_piece[index] = piece[rotation_axis2]
                elif index == rotation_axis2:
                    new_piece[index] = -piece[rotation_axis1]
                else:
                    new_piece[index] = piece[index]
            new_pieces.append(new_piece)

        self.pieces = new_pieces.copy()

    # this will check if a piece is colliding with the outer walls or any placed blocks
    def check_intersection(self, placed_blocks, grid_size):
        moved_pieces = self.get_moved_pieces()

        for piece in moved_pieces:
            for axis in range(4):
                # If a piece is above the grid in the fourth dimension,
                # it is not out of the boundaries, so do not check that
                if (piece[axis] < 0 or piece[axis] >= grid_size[axis]
                        and not (axis == 3 and piece[axis] >= grid_size[axis])):
                    return False
            for placed_piece in placed_blocks:
                if piece == placed_piece:
                    return False

        return True

    # this will return coordinates of a piece including its offset
    def get_moved_pieces(self):
        moved_pieces = []

        for piece in self.pieces:
            moved_pieces.append([piece[index] + self.offset[index] for index in range(4)])

        return moved_pieces
