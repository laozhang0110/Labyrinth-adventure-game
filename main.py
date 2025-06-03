import pygame
from game.map import Map
from game.player import Player
from game.enemy import Enemy
from game.level import generate_maze

pygame.init()

# Initialize window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)  # For game over message

# Game mode: PRESET or RANDOM
GAME_MODE = "RANDOM"

if GAME_MODE == "PRESET":
    level_files = ["config/level1.json", "config/level2.json"]
    current_level = 0
else:
    level_files = []
    current_level = 0


def load_level(index):
    if GAME_MODE == "PRESET":
        game_map = Map(level_files[index])
    else:
        level_data = generate_maze(10, 10)
        game_map = Map(level_data)

    start_x, start_y = game_map.start_pos
    player = Player(start_x, start_y)
    enemy = Enemy(5, 5)
    return game_map, player, enemy


game_map, player, enemy = load_level(current_level)
score = 100
start_ticks = pygame.time.get_ticks()
completed_levels = 0
game_over = False
game_result = ""

# UI positioning
info_margin_right = 20
info_line_height = 40

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not game_over:  # Press R to regenerate level
                game_map, player, enemy = load_level(current_level)
                start_ticks = pygame.time.get_ticks()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            result = player.move(0, -1, game_map)
        elif keys[pygame.K_s]:
            result = player.move(0, 1, game_map)
        elif keys[pygame.K_a]:
            result = player.move(-1, 0, game_map)
        elif keys[pygame.K_d]:
            result = player.move(1, 0, game_map)
        else:
            result = "PLAYING"

        # Enemy movement and collision
        enemy.update(game_map, (player.grid_x, player.grid_y))
        if (player.grid_x, player.grid_y) == (enemy.grid_x, enemy.grid_y):
            game_over = True
            game_result = "Caught by enemy!"

        # Check score
        if score <= 0:
            game_over = True
            game_result = "Score reached zero!"

        if result == "WIN":
            completed_levels += 1
            if GAME_MODE == "PRESET":
                current_level += 1
                if current_level >= len(level_files):
                    game_over = True
                    game_result = "All levels completed!"
                else:
                    game_map, player, enemy = load_level(current_level)
                    start_ticks = pygame.time.get_ticks()
            else:
                game_map, player, enemy = load_level(current_level)
                start_ticks = pygame.time.get_ticks()
        elif result == "TRAP":
            score = max(0, score - 10)

    # Draw map and characters
    game_map.draw(screen)
    player.draw(screen)
    enemy.draw(screen)

    # Display game info (right side)
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000


    def get_right_x(text_surface):
        return screen_width - text_surface.get_width() - info_margin_right


    time_text = f"Time: {seconds}s"
    score_text = f"Score: {score}"
    mode_text = f"Mode: {GAME_MODE}"
    levels_text = f"Levels: {completed_levels}"

    time_surf = font.render(time_text, True, (255, 255, 255))
    score_surf = font.render(score_text, True, (255, 255, 255))
    mode_surf = font.render(mode_text, True, (255, 255, 255))
    levels_surf = font.render(levels_text, True, (255, 255, 255))

    screen.blit(time_surf, (get_right_x(time_surf), 10))
    screen.blit(score_surf, (get_right_x(score_surf), 10 + info_line_height))
    screen.blit(mode_surf, (get_right_x(mode_surf), 10 + info_line_height * 2))
    screen.blit(levels_surf, (get_right_x(levels_surf), 10 + info_line_height * 3))

    # Game over display
    if game_over:
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Result text
        result_text1 = large_font.render("GAME OVER", True, (255, 255, 255))
        result_text2 = font.render(f"Reason: {game_result}", True, (255, 255, 255))
        result_text3 = font.render(f"Levels completed: {completed_levels}", True, (255, 255, 255))
        result_text4 = font.render("Press ESC to quit", True, (255, 255, 255))

        screen.blit(result_text1, (screen_width // 2 - result_text1.get_width() // 2, screen_height // 2 - 100))
        screen.blit(result_text2, (screen_width // 2 - result_text2.get_width() // 2, screen_height // 2 - 30))
        screen.blit(result_text3, (screen_width // 2 - result_text3.get_width() // 2, screen_height // 2 + 10))
        screen.blit(result_text4, (screen_width // 2 - result_text4.get_width() // 2, screen_height // 2 + 80))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(10)

# Console output after game ends
print("\n=== GAME STATISTICS ===")
print(f"Game mode: {GAME_MODE}")
print(f"Levels completed: {completed_levels}")
print(f"Final score: {score}")
print(f"Play time: {seconds} seconds")
print(f"End reason: {game_result}")

pygame.quit()