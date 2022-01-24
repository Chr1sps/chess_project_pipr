import pygame
from io import BytesIO


def load_svg_resize(filename, piece_size):
    svg_string = open(filename, "rt").read()

    width_pos_start = svg_string.find("width=") + 7
    width_pos_end = width_pos_start

    while svg_string[width_pos_end] != '"':
        width_pos_end += 1

    width = int(svg_string[width_pos_start:width_pos_end])

    height_pos_start = svg_string.find("height=") + 8
    height_pos_end = height_pos_start

    while svg_string[height_pos_end] != '"':
        height_pos_end += 1

    start = svg_string.find("<svg") + 4

    svg_string = (
        svg_string[:start]
        + f' transform="scale({piece_size/width})"'
        + svg_string[start:width_pos_start]
        + str(piece_size)
        + svg_string[width_pos_end:height_pos_start]
        + str(piece_size)
        + svg_string[height_pos_end:]
    )

    return pygame.image.load(BytesIO(svg_string.encode()))
