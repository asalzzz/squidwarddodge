import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squidward Dodge")
clock = pygame.time.Clock()

# Load sounds
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)
hit_sound = pygame.mixer.Sound("hit.wav")

# Load images
player_img = pygame.image.load("squidward.png")
player_img = pygame.transform.scale(player_img, (120, 120))
jelly_img = pygame.image.load("jellyfish.png")
jelly_img = pygame.transform.scale(jelly_img, (60, 60))

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# Player
player_x = WIDTH // 2
player_y = HEIGHT - 130
player_speed = 6

# Jellyfish
num_jellyfish = 5
def create_jellyfish():
    return [
        {"x": random.randint(0, WIDTH - 60),
         "y": random.randint(-300, -60),
         "speed": random.randint(3, 7)}
        for _ in range(num_jellyfish)
    ]

jellyfish = create_jellyfish()

# Game state
score = 0
game_state = "title"

def draw_centered_text(text, y, color=(0, 0, 0), font_obj=font):
    render = font_obj.render(text, True, color)
    x = WIDTH // 2 - render.get_width() // 2
    screen.blit(render, (x, y))

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill((173, 216, 230))  # Light blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Title screen → start game
        if game_state == "title":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "playing"
                score = 0
                player_x = WIDTH // 2
                jellyfish = create_jellyfish()

        # Game Over → restart game
        if game_state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = "playing"
                score = 0
                player_x = WIDTH // 2
                jellyfish = create_jellyfish()

    keys = pygame.key.get_pressed()

    if game_state == "title":
        draw_centered_text("Squidward vs. Jellyfish", HEIGHT // 2 - 100, (0, 0, 128), big_font)
        draw_centered_text("Press SPACE to start", HEIGHT // 2, (0, 0, 0))
        draw_centered_text("Use arrow keys to move. Avoid jellyfish!", HEIGHT // 2 + 50, (0, 0, 0))

    elif game_state == "playing":
        # Movement
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 120:
            player_x += player_speed

        # Update and draw jellyfish
        for jelly in jellyfish:
            jelly["y"] += jelly["speed"]
            if jelly["y"] > HEIGHT:
                jelly["y"] = random.randint(-100, -40)
                jelly["x"] = random.randint(0, WIDTH - 60)
                jelly["speed"] = random.randint(3, 7)
                score += 1

            player_rect = pygame.Rect(player_x, player_y, 120, 120)
            jelly_rect = pygame.Rect(jelly["x"], jelly["y"], 60, 60)
            if player_rect.colliderect(jelly_rect):
                hit_sound.play()
                game_state = "game_over"

            screen.blit(jelly_img, (jelly["x"], jelly["y"]))

        screen.blit(player_img, (player_x, player_y))
        # Score aligned top-left, so keep it there
        text_score = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text_score, (10, 10))

    elif game_state == "game_over":
        draw_centered_text("Game Over!", HEIGHT // 2 - 90, (255, 0, 0), big_font)
        draw_centered_text(f"Final Score: {score}", HEIGHT // 2 - 30)
        draw_centered_text("rip squid", HEIGHT // 2 + 10, (255, 0, 0), big_font)
        draw_centered_text("Press R to Restart", HEIGHT // 2 + 70)

    pygame.display.flip()

pygame.quit()
sys.exit()

# python3 game.py