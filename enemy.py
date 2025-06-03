import random
import pygame
from collections import deque
from game.map import TILE_SIZE

class Enemy:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.color = (138, 43, 226)
        self.move_cooldown = 0

    def update(self, game_map, player_pos):
        self.move_cooldown += 1
        if self.move_cooldown >= 10:
            path = self.bfs_path((self.grid_x, self.grid_y), player_pos, game_map)
            if len(path) > 1:
                self.grid_x, self.grid_y = path[1]
            self.move_cooldown = 0

    def bfs_path(self, start, end, game_map):
        queue = deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == end:
                break
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < game_map.width and 0 <= ny < game_map.height and
                        game_map.tiles[ny][nx] != "W" and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited[(nx, ny)] = current
        path = []
        node = end
        while node in visited and node is not None:
            path.append(node)
            node = visited[node]
        return path[::-1]

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.color,
            (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )