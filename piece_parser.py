import piece

'''
Here is an example of how pieces are stored
0:0,0,0,0|0,0,0,0;-1,0,0,0;1,0,0,0;0,0,1,0|0,0,0,0
The template for pieces are:
ID:Centre|BlockCoords|ExtraOffset
Block coordinates are separated by semicolons.
ExtraOffset isn't the offset used for the piece. Every piece will spawn at 1,1,1,W-1 (W being the 4d height of the grid)
If, for some reason, a piece intersects with the wall, the offset can be changed so that it fits.
'''

def return_pieces(text_lines):
    piece_list = []

    for line in text_lines:
        id_split = line.split(":")
        piece_id = int(id_split[0])
        centre_split = id_split[1].split("|")
        centre = [int(coord) for coord in centre_split[0].split(",")]
        extra_offset = [int(coord) for coord in centre_split[2].split(",")]
        pieces_split = centre_split[1].split(";")
        pieces = [[int(coord) for coord in piece.split(",")] for piece in pieces_split]

        piece_list.append(piece.Piece(piece_id, centre, pieces, [0,0,0,0], extra_offset))

    return piece_list
