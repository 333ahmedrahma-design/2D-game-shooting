import pygame
import sys
import math

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
GREEN = (50, 255, 50)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Shooting Game - 2D Enemy Pursuit")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 64)

# --- Game Variables ---
score = 0
player_health = 3
game_over = False

# Player Setup
player_size = 40
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 5

# Enemy Setup
enemy_size = 40
enemy_x = 100
enemy_y = 100
enemy_speed = 2.5  # Slightly adjusted speed for smooth 2D tracking

# Bullet Setup
bullets = []
bullet_width = 6
bullet_height = 15
bullet_speed = 7

# Reward Setup
reward_rect = None
reward_size = 25

# Game Loop Flag
running = True

while running:
    # 1. Event Handling (Inputs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet_x = player_x + player_size // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
            
            # Restart game on 'R' if game over
            if event.key == pygame.K_r and game_over:
                score = 0
                player_health = 3
                game_over = False
                player_x = SCREEN_WIDTH // 2 - player_size // 2
                player_y = SCREEN_HEIGHT - 100
                enemy_x = 100
                enemy_y = 100
                reward_rect = None
                bullets.clear()

    if not game_over:
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
        
        # Enemy AI: True 2D Chase (Tracks both X and Y toward the player)
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            # Normalize direction vector and multiply by speed
            enemy_x += (dx / distance) * enemy_speed
            enemy_y += (dy / distance) * enemy_speed

        # Update Bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # 3. Collision Detection
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

        # Check bullet hits enemy
        for bullet in bullets[:]:
            if bullet.colliderect(enemy_rect):
                bullets.remove(bullet)
                
                # Spawn Reward at enemy position
                reward_rect = pygame.Rect(
                    enemy_x + (enemy_size // 2) - (reward_size // 2),
                    enemy_y + (enemy_size // 2) - (reward_size // 2),
                    reward_size,
                    reward_size
                )
                
                # Reset enemy position to a random corner or top
                enemy_x = 100
                enemy_y = 50

        # Check player collects reward
        if reward_rect is not None and player_rect.colliderect(reward_rect):
            score += 10
            reward_rect = None

        # Check enemy hits player (Health loss)
        if player_rect.colliderect(enemy_rect):
            player_health -= 1
            print(f"Player hit! Health remaining: {player_health}")
            
            # Reset enemy position so it doesn't instantly drain all health
            enemy_x = 100
            enemy_y = 50
            
            if player_health <= 0:
                game_over = True

    # 4. Drawing / Rendering
    screen.fill(BLACK)

    if not game_over:
        # Draw Player
        pygame.draw.rect(screen, BLUE, player_rect)
        # Draw Enemy
        pygame.draw.rect(screen, RED, enemy_rect)
        # Draw Reward
        if reward_rect is not None:
            pygame.draw.rect(screen, GREEN, reward_rect)
        # Draw Bullets
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)
    else:
        # Game Over Screen
        go_surface = game_over_font.render("GAME OVER", True, RED)
        restart_surface = font.render("Press 'R' to Restart", True, WHITE)
        screen.blit(go_surface, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_surface, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 10))

    # Draw HUD (Score & Health)
    score_surface = font.render(f"Score: {score}", True, WHITE)
    health_surface = font.render(f"Health: {player_health}", True, WHITE)
    screen.blit(score_surface, (20, 20))
    screen.blit(health_surface, (20, 60))

    # Refresh screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()