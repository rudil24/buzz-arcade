import asyncio
import pygame
import sys

# Constants matching 3:4 Vertical Arcade Aspect Ratio
WIDTH = 600
HEIGHT = 800
FPS = 60

# Colors
BLACK = (10, 15, 30)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 243, 255)
NEON_PINK = (255, 0, 234)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IceOut")
clock = pygame.time.Clock()

# TODO: Load family and villain assets here

async def main():
    running = True
    
    # Paddle setup
    paddle_width = 100
    paddle_height = 20
    paddle_x = (WIDTH - paddle_width) // 2
    paddle_y = HEIGHT - 50
    paddle_speed = 8
    
    # Ball setup
    ball_x = WIDTH // 2
    ball_y = paddle_y - 20
    ball_dx = 5
    ball_dy = -5
    ball_radius = 8

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed
            
        # Basic Ball Bounds Logic
        ball_x += ball_dx
        ball_y += ball_dy
        
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1
            
        # Basic Paddle Collision
        if ball_y + ball_radius >= paddle_y and ball_y <= paddle_y + paddle_height:
            if ball_x >= paddle_x and ball_x <= paddle_x + paddle_width:
                ball_dy *= -1
                # Add slight random english based on paddle hit pos later

        # Rendering
        screen.fill(BLACK)
        
        # Draw Paddle
        pygame.draw.rect(screen, NEON_BLUE, (paddle_x, paddle_y, paddle_width, paddle_height), border_radius=5)
        
        # Draw Ball
        pygame.draw.circle(screen, WHITE, (ball_x, int(ball_y)), ball_radius)
        
        # Placeholder text
        font = pygame.font.Font(None, 36)
        text = font.render("Attract Mode - Family Loading...", True, NEON_PINK)
        screen.blit(text, (WIDTH//2 - 180, HEIGHT//2))

        pygame.display.flip()
        
        # Required for pygbag / WASM async loop
        await asyncio.sleep(0)
        clock.tick(FPS)

if __name__ == "__main__":
    asyncio.run(main())
