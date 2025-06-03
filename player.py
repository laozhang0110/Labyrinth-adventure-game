import pygame
from game.map import TILE_SIZE

class Player:
    def __init__(self, start_x, start_y):
        self.grid_x = start_x
        self.grid_y = start_y
        self.size = TILE_SIZE
        self.color = (0, 225, 255)

    def move(self, dx, dy, game_map):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if 0 <= new_y < len(game_map.tiles) and 0 <= new_x < len(game_map.tiles[0]):
            target = game_map.tiles[new_y][new_x]
            if target != "W":
                self.grid_x = new_x
                self.grid_y = new_y
                if target == "E":
                    return "WIN"
                elif target == "T":
                    return "TRAP"
                elif target == "M":
                    pygame.time.delay(200)
        return "PLAYING"

    def draw(self, screen):
        x = self.grid_x * TILE_SIZE
        y = self.grid_y * TILE_SIZE
        pygame.draw.rect(screen, self.color, (x, y, self.size, self.size))