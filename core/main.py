import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 75, 75)
YELLOW = (255, 220, 50)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Shooting Game - Basics")
clock = pygame.time.Clock()

# --- Game Entities ---

# Player Setup
player_size = 40
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 5

# Enemy Setup
enemy_size = 40
enemy_x = SCREEN_WIDTH // 2 - enemy_size // 2
enemy_y = 100
enemy_speed = 2

# Bullet Setup
bullets = []  # List to store active bullets
bullet_width = 6
bullet_height = 15
bullet_speed = 7

# Game Loop Flag
running = True

while running:
    # 1. Event Handling (Inputs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Shoot bullet on Spacebar press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create bullet at player's top-center
                bullet_x = player_x + player_size // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    # Continuous Key Presses for Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed

    # Keep player inside screen boundaries
    player_x = max(0, min(SCREEN_WIDTH - player_size, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - player_size, player_y))

    # 2. Update Game Logic
    
    # Simple Enemy AI: Chase the player horizontally
    if enemy_x < player_x:
        enemy_x += enemy_speed
    elif enemy_x > player_x:
        enemy_x -= enemy_speed

    # Update Bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        # Remove bullet if it goes off screen
        if bullet.y < 0:
            bullets.remove(bullet)

    # 3. Collision Detection
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

    # Check bullet hits enemy
    for bullet in bullets[:]:
        if bullet.colliderect(enemy_rect):
            bullets.remove(bullet)
            # Reset enemy position for testing purposes
            enemy_x = SCREEN_WIDTH // 2 - enemy_size // 2
            enemy_y = 50
            print("Monster hit!")

    # Check enemy hits player
    if player_rect.colliderect(enemy_rect):
        print("Player hit by monster!")

    # 4. Drawing / Rendering
    screen.fill(BLACK) # Clear screen with black background

    # Draw Player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw Enemy
    pygame.draw.rect(screen, RED, enemy_rect)

    # Draw Bullets
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    # Refresh screen
    pygame.display.flip()

    # Cap framerate to 60 FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()