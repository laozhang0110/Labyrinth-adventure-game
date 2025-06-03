import pygame
import json

TILE_SIZE = 60

COLOR_MAP = {
    "0": (255, 255, 255),  # Path (white)
    "W": (0, 0, 0),        # Wall (black)
    "S": (0, 255, 0),      # Start (green)
    "E": (255, 0, 0),      # End (red)
    "T": (128, 128, 128),  # Trap (gray)
    "M": (134, 70, 29)     # Marsh (brown)
}

class Map:
    def __init__(self, data):
        if isinstance(data, str):  # If it's a file path
            with open(data, "r") as f:
                data = json.load(f)
        self.tiles = data["tiles"]
        self.width = data["width"]
        self.height = data["height"]
        self.start_pos = data["start"]
        self.end_pos = data["end"]

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                color = COLOR_MAP.get(tile, (150, 150, 150))
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))