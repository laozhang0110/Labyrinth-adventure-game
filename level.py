import json
import random
from collections import deque


def generate_maze(width, height):
    # Initialize all cells as walls
    maze = [["W" for _ in range(width)] for _ in range(height)]

    # Set start and end positions
    start_x, start_y = 0, 0
    end_x, end_y = width - 1, height - 1

    # Mark start and end
    maze[start_y][start_x] = "S"
    maze[end_y][end_x] = "E"

    # Generate maze using DFS
    stack = [(start_x, start_y)]
    visited = set([(start_x, start_y)])

    while stack:
        x, y = stack[-1]
        neighbors = []

        # Check four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                neighbors.append((nx, ny, x + dx, y + dy))

        if neighbors:
            nx, ny, wx, wy = random.choice(neighbors)
            maze[wy][wx] = "0"  # Break wall
            maze[ny][nx] = "0"  # Mark as path
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()

    # Ensure path exists from start to end
    if not is_path_available(maze, (start_x, start_y), (end_x, end_y)):
        create_path(maze, (start_x, start_y), (end_x, end_y))

    # Add traps and marshes randomly
    for y in range(height):
        for x in range(width):
            if maze[y][x] == "0" and (x, y) != (start_x, start_y) and (x, y) != (end_x, end_y):
                if random.random() < 0.1:  # 10% chance for trap
                    maze[y][x] = "T"
                elif random.random() < 0.1:  # 10% chance for marsh
                    maze[y][x] = "M"

    return {
        "width": width,
        "height": height,
        "start": [start_x, start_y],
        "end": [end_x, end_y],
        "tiles": maze
    }


def is_path_available(maze, start, end):
    width, height = len(maze[0]), len(maze)
    visited = set()
    queue = deque([start])

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height and
                    maze[ny][nx] != "W" and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny))

    return False


def create_path(maze, start, end):
    x, y = start
    end_x, end_y = end

    while (x, y) != (end_x, end_y):
        if x < end_x:
            x += 1
        elif x > end_x:
            x -= 1
        elif y < end_y:
            y += 1
        elif y > end_y:
            y -= 1

        if maze[y][x] == "W":
            maze[y][x] = "0"

        # Randomly break adjacent walls for variety
        for dx, dy in random.sample([(0, 1), (1, 0), (0, -1), (-1, 0)], 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == "W":
                maze[ny][nx] = "0"


def save_level_to_file(level, filename):
    with open(filename, "w") as f:
        json.dump(level, f, indent=2)


if __name__ == "__main__":
    level = generate_maze(10, 10)
    save_level_to_file(level, "config/level_generated.json")
    print("Maze generated and saved to config/level_generated.json")