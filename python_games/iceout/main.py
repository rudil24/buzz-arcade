import asyncio
import pygame
import random
import sys
import os
import math

# Bonus points for catching the falling family member
CATCH_BONUS = {1: 500, 2: 1000, 3: 1500, 4: 2000}
# Family sprite per level
FAMILY_SPRITE = {1: 'fam_son', 2: 'fam_daughter', 3: 'fam_mom', 4: 'fam_dad'}

# Constants
WIDTH = 600
HEIGHT = 800
FPS = 60

# Colors
BLACK = (10, 15, 30)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 243, 255)
NEON_PINK = (255, 0, 234)
NEON_RED = (255, 0, 60)
ICE_COLORS = [(0, 243, 255, 150), (100, 200, 255, 150), (200, 100, 255, 150), (255, 100, 200, 150)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IceOut")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

IMAGES = {}
def load_images():
    sprites = ['paddle', 'ball', 'block_blue', 'block_purple', 'block_green',
               'fam_dad', 'fam_mom', 'fam_son', 'fam_daughter']
    for i in range(1, 5):
        sprites.append(f'villain{i}')

        
    for spr in sprites:
        try:
            img = pygame.image.load(f"assets/sprites/{spr}.png").convert_alpha()
            IMAGES[spr] = img
        except Exception as e:
            print(f"Could not load {spr}.png:", e)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

SCORES_FILE = "highscores.txt"
ALLOWED_INITIALS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?&')

def load_scores():
    """Returns list of (initials, score) tuples, sorted high-first."""
    entries = []
    try:
        with open(SCORES_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if ',' in line:
                    parts = line.split(',', 1)
                    try:
                        entries.append((parts[0], int(parts[1])))
                    except ValueError:
                        pass
                elif line.isdigit():  # legacy plain numbers
                    entries.append(('???', int(line)))
    except Exception:
        pass
    return sorted(entries, key=lambda x: x[1], reverse=True)[:10]

def is_top_10(score):
    scores = load_scores()
    return len(scores) < 10 or score > scores[-1][1]

def save_entry(initials, score):
    entries = load_scores()
    entries.append((initials[:3].upper(), score))
    entries = sorted(entries, key=lambda x: x[1], reverse=True)[:10]
    try:
        with open(SCORES_FILE, 'w') as f:
            for ini, s in entries:
                f.write(f"{ini},{s}\n")
    except Exception as e:
        print("Could not save score:", e)

def draw_zone_text(surface, text, font_size, alpha, y):
    """Draw translucent italic-style text centred horizontally at y."""
    zfont = pygame.font.Font(None, font_size)
    surf = zfont.render(text, True, WHITE)
    # Simulate italic by shearing horizontally (pixel-by-pixel row shift)
    w, h = surf.get_size()
    shear = 0.28
    new_w = w + int(h * shear) + 2
    italic_surf = pygame.Surface((new_w, h), pygame.SRCALPHA)
    for row in range(h):
        x_off = int(shear * (h - row))
        italic_surf.blit(surf, (x_off, row), (0, row, w, 1))
    italic_surf.set_alpha(alpha)
    rect = italic_surf.get_rect(center=(WIDTH // 2, y))
    surface.blit(italic_surf, rect)

def draw_spacebar_icon(surface, cx, cy, w=40, h=16, color=(200,200,200)):
    """Draw the international spacebar symbol (U-bracket) centred at cx,cy."""
    thick = 4
    # Bottom bar
    pygame.draw.rect(surface, color, (cx - w//2, cy + h//2 - thick, w, thick))
    # Left leg
    pygame.draw.rect(surface, color, (cx - w//2, cy - h//2, thick, h))
    # Right leg
    pygame.draw.rect(surface, color, (cx + w//2 - thick, cy - h//2, thick, h))

def draw_pause_overlay(surface, font, large_font):
    # Semi-transparent dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    # Dialog box
    bw, bh = 400, 200
    bx, by = (WIDTH - bw)//2, (HEIGHT - bh)//2
    pygame.draw.rect(surface, (20, 30, 60), (bx, by, bw, bh), border_radius=12)
    pygame.draw.rect(surface, NEON_BLUE, (bx, by, bw, bh), width=2, border_radius=12)
    draw_text("BACK TO CONCOURSE?", font, WHITE, surface, WIDTH//2, by + 45)
    # ESC row
    esc_font = pygame.font.Font(None, 28)
    draw_text("ESC  ·  QUIT", esc_font, NEON_RED, surface, WIDTH//2, by + 100)
    # Spacebar icon + CONTINUE
    draw_spacebar_icon(surface, WIDTH//2 - 60, by + 148)
    draw_text("CONTINUE", esc_font, NEON_BLUE, surface, WIDTH//2 + 30, by + 148)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 50
        self.speed = 8
        self.color = NEON_BLUE

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        if 'paddle' in IMAGES:
            img = pygame.transform.scale(IMAGES['paddle'], (self.width, self.height))
            surface.blit(img, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=5)

class Ball:
    def __init__(self, speed_mult):
        self.radius = 8
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.base_speed = 5 * speed_mult
        self.dx = random.choice([-1, 1]) * self.base_speed
        self.dy = -self.base_speed
        self.color = WHITE
        self.active = False

    def move(self):
        if not self.active:
            return
        self.x += self.dx
        self.y += self.dy

        # Wall collisions
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx *= -1
            # add tiny jitter so ball never stays perfectly vertical
            self.dx += random.uniform(-0.3, 0.3)
        if self.y - self.radius <= 0:
            self.dy *= -1

        # Enforce minimum horizontal speed so ball can't loop vertically
        MIN_DX = 1.5
        if abs(self.dx) < MIN_DX:
            self.dx = MIN_DX if self.dx >= 0 else -MIN_DX

    def draw(self, surface):
        if 'ball' in IMAGES:
            img = pygame.transform.scale(IMAGES['ball'], (self.radius*2, self.radius*2))
            surface.blit(img, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Block:
    def __init__(self, x, y, width, height, color_name):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_name = color_name
        self.active = True

    def draw(self, surface):
        if self.active:
            if self.color_name in IMAGES:
                img = pygame.transform.scale(IMAGES[self.color_name], (self.rect.width, self.rect.height))
                surface.blit(img, (self.rect.x, self.rect.y))
            else:
                s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                s.fill(WHITE)
                pygame.draw.rect(s, WHITE, s.get_rect(), 1)
                surface.blit(s, (self.rect.x, self.rect.y))

class FamilyMember:
    def __init__(self, level=1):
        self.width = 36 if level == 1 else 54
        self.height = 48 if level == 1 else 72
        self.x = WIDTH // 2
        self.y = 100  # Above blocks
        self.speed = 2
        self.direction = 1
        self.falling = False
        self.rescued = False
        self.color = NEON_PINK
        self.sprite_key = FAMILY_SPRITE.get(level, 'fam_son')
        self.level = level
        self.catch_scored = False

    def update(self, blocks):
        if self.rescued:
            return

        if not self.falling:
            self.x += self.speed * self.direction
            if self.x <= 0 or self.x >= WIDTH - self.width:
                self.direction *= -1

            # Check if there are active blocks directly below
            supported = False
            feet_y = self.y + self.height
            for b in blocks:
                if b.active and b.rect.top >= feet_y and (b.rect.left < self.x + self.width and b.rect.right > self.x):
                    supported = True
                    break
            
            # If no blocks support, start falling
            blocks_exist = any(b.active for b in blocks)
            if not supported and blocks_exist:
                pass
            
            # Drop when no active blocks remain in the vertical column spanning their width.
            column_supported = False
            for b in blocks:
                if b.active and b.rect.left < self.x + self.width and b.rect.right > self.x:
                    column_supported = True
                    break
            
            if not column_supported:
                self.falling = True

        else:
            self.y += 5
            if self.y > HEIGHT:
                self.rescued = True  # fell off — remove, no bonus

    def draw(self, surface):
        if not self.rescued:
            if self.sprite_key in IMAGES:
                img = pygame.transform.scale(IMAGES[self.sprite_key], (self.width, self.height))
                if self.direction < 0:
                    img = pygame.transform.flip(img, True, False)
                surface.blit(img, (int(self.x), int(self.y)))
            else:
                pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height))
                draw_text("Fam", pygame.font.Font(None, 20), WHITE, surface, int(self.x + self.width/2), int(self.y - 10))

class Villain:
    def __init__(self, level):
        # L3 & L4 villains are 25% bigger
        if level >= 3:
            self.width = 90
            self.height = 120
        else:
            self.width = 72
            self.height = 96
        self.y = HEIGHT // 2 - self.height // 2
        self.direction = random.choice([-1, 1])
        self.x = -self.width if self.direction == 1 else WIDTH
        self.speed = 1.5 + level * 0.5  # slower: was 3+level
        self.active = True
        self.level = level

    def update(self):
        if not self.active:
            return
        self.x += self.speed * self.direction
        if (self.direction == 1 and self.x > WIDTH) or (self.direction == -1 and self.x < -self.width):
            self.active = False

    def draw(self, surface):
        if not self.active:
            return
        v_key = f'villain{(self.level - 1) % 4 + 1}'
        if v_key in IMAGES:
            img = pygame.transform.scale(IMAGES[v_key], (self.width, self.height))
            if self.direction < 0:
                img = pygame.transform.flip(img, True, False)
            surface.blit(img, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(surface, (255, 0, 0), (int(self.x), int(self.y), self.width, self.height))

async def main():
    load_images()
    
    clock = pygame.time.Clock()
    state = "START"
    level = 1
    score = 0
    lives = 3
    
    paddle = Paddle()
    ball = Ball(1)
    blocks = []
    family_member = None
    villain = None
    villain_timer = 0
    current_initials = ""

    def init_level(lvl):
        nonlocal blocks, family_member, villain, villain_timer, paddle, ball
        blocks = []
        rows = 4 + lvl
        cols = 8
        block_w = WIDTH // cols
        block_h = 30
        start_y = 200
        color_names = ['block_blue', 'block_purple', 'block_green', 'block_blue']
        for r in range(rows):
            c_name = color_names[r % len(color_names)]
            for c in range(cols):
                blocks.append(Block(c * block_w, start_y + r * block_h, block_w - 2, block_h - 2, c_name))
        family_member = FamilyMember(lvl)
        villain = None
        villain_timer = 0
        paddle = Paddle()
        ball = Ball(1 + (lvl * 0.2))
        ball.active = False
        ball.x = paddle.x + paddle.width // 2
        ball.y = paddle.y - ball.radius - 1

    init_level(level)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "PLAYING":
                        state = "PAUSED"
                    elif state == "PAUSED":
                        sys.exit()  # ESC again → exit to concourse
                elif state == "PAUSED" and event.key == pygame.K_SPACE:
                    state = "PLAYING"
                # Dev shortcuts: F1-F4 jump to level
                elif event.key in (pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4):
                    dev_lvl = {pygame.K_F1:1, pygame.K_F2:2, pygame.K_F3:3, pygame.K_F4:4}[event.key]
                    level = dev_lvl
                    init_level(level)
                    state = "PLAYING"
                    ball.active = True
                if state == "START" and event.key == pygame.K_SPACE:
                    state = "PLAYING"
                    ball.active = True
                elif state == "PLAYING" and event.key == pygame.K_SPACE and not ball.active:
                    ball.active = True
                elif state == "GAME_OVER" and event.key == pygame.K_SPACE:
                    if is_top_10(score):
                        state = "ENTER_INITIALS"
                        current_initials = ""
                    else:
                        level = 1; score = 0; lives = 3
                        init_level(level); state = "START"
                elif state == "LEVEL_CLEARED" and event.key == pygame.K_SPACE:
                    if level < 4:
                        level += 1
                        init_level(level)
                        state = "START"
                    else:
                        state = "GAME_WON"
                elif state == "GAME_WON" and event.key == pygame.K_SPACE:
                    if is_top_10(score):
                        state = "ENTER_INITIALS"
                        current_initials = ""
                    else:
                        level = 1; score = 0; lives = 3
                        init_level(level); state = "START"
                # Initials entry
                elif state == "ENTER_INITIALS":
                    if event.key == pygame.K_BACKSPACE:
                        current_initials = current_initials[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        # Confirm with at least 1 char (pad with underscores)
                        if len(current_initials) > 0:
                            save_entry(current_initials.ljust(3, '_')[:3], score)
                            level = 1; score = 0; lives = 3
                            init_level(level); state = "START"
                    else:
                        ch = pygame.key.name(event.key).upper()
                        if len(ch) == 1 and ch in ALLOWED_INITIALS and len(current_initials) < 3:
                            current_initials += ch
                            # NO auto-confirm — always require ENTER to submit

        keys = pygame.key.get_pressed()

        if state in ("PLAYING", "PAUSED"):
            if state == "PLAYING":
                paddle.move(keys)
            
            if not ball.active:
                ball.x = paddle.x + paddle.width // 2
                ball.y = paddle.y - ball.radius - 1
            else:
                ball.move()

            # Paddle Collision
            if ball.dy > 0 and ball.y + ball.radius >= paddle.y and ball.y - ball.radius <= paddle.y + paddle.height:
                if ball.x >= paddle.x and ball.x <= paddle.x + paddle.width:
                    ball.dy *= -1
                    hit_pos = (ball.x - paddle.x) / paddle.width  # 0.0 (left) to 1.0 (right)
                    # Non-linear curve: sign * t^2 gives much sharper corners
                    t = hit_pos - 0.5          # -0.5 … +0.5
                    ball.dx = 16 * t * abs(t)  # quadratic: ±0 center, ±4 edge
                    # Clamp so we never go totally flat
                    MIN_DX = 1.0
                    if abs(ball.dx) < MIN_DX:
                        ball.dx = MIN_DX if ball.dx >= 0 else -MIN_DX

            # Block Collision
            for b in blocks:
                if b.active:
                    if b.rect.collidepoint(ball.x, ball.y - ball.radius) or b.rect.collidepoint(ball.x, ball.y + ball.radius):
                        ball.dy *= -1
                        b.active = False
                        score += 10
                        break
                    elif b.rect.collidepoint(ball.x - ball.radius, ball.y) or b.rect.collidepoint(ball.x + ball.radius, ball.y):
                        ball.dx *= -1
                        b.active = False
                        score += 10
                        break

            # Villain logic
            villain_timer += 1
            if villain_timer > 600 and villain is None:
                villain = Villain(level)
            
            if villain and villain.active:
                villain.update()
                # Villain Collision — ball bounces back like hitting a brick
                villain_rect = pygame.Rect(int(villain.x), int(villain.y), villain.width, villain.height)
                ball_rect = pygame.Rect(int(ball.x - ball.radius), int(ball.y - ball.radius),
                                        ball.radius * 2, ball.radius * 2)
                if ball_rect.colliderect(villain_rect):
                    ball.dy *= -1  # bounce vertically
                    # nudge ball out of villain to prevent sticking
                    ball.y += ball.dy * 2
                    score += 500
                    villain.active = False
                    villain = None
                    villain_timer = 0
            elif villain and not villain.active:
                villain = None

            # Check if falling family member is caught by paddle
            if family_member.falling and not family_member.rescued and not family_member.catch_scored:
                fam_rect = pygame.Rect(int(family_member.x), int(family_member.y),
                                       family_member.width, family_member.height)
                paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
                if fam_rect.colliderect(paddle_rect):
                    bonus = CATCH_BONUS.get(level, 500)
                    score += bonus
                    family_member.catch_scored = True
                    family_member.rescued = True  # stop drawing

            family_member.update(blocks)

            # Level clears when all blocks are gone
            if not any(b.active for b in blocks):
                state = "LEVEL_CLEARED"

            # Check dead ball
            if ball.y > HEIGHT:
                lives -= 1
                if lives <= 0:
                    state = "GAME_OVER"
                else:
                    ball.active = False

            # All blocks gone → make family member fall if still walking
            if not any(b.active for b in blocks):
                family_member.falling = True

        screen.fill(BLACK)

        if state == "START":
            if 'title' in IMAGES:
                t_img = IMAGES['title']
                t_rect = t_img.get_rect(center=(WIDTH//2, HEIGHT//3))
                screen.blit(t_img, t_rect)
            else:
                draw_text("ICE-OUT", large_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//3)
            
            draw_text("PRESS SPACE TO START", font, NEON_PINK, screen, WIDTH//2, HEIGHT//2 + 80)
            draw_text(f"Level {level}", font, WHITE, screen, WIDTH//2, HEIGHT//2 + 130)
            # High scores
            hi_font = pygame.font.Font(None, 26)
            scores = load_scores()
            if scores:
                draw_text("HIGH SCORES", hi_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//2 + 185)
                for i, s in enumerate(scores[:5]):
                    draw_text(f"{i+1}. {s:,}", hi_font, (180,180,180), screen, WIDTH//2, HEIGHT//2 + 210 + i*22)
            
        elif state in ["PLAYING", "LEVEL_CLEARED", "GAME_OVER", "GAME_WON", "PAUSED"]:
            # Background zone label above bricks (drawn first, behind sprites)
            draw_zone_text(screen, '"CRIMINAL" CONFINEMENT', 46, 28, 130)
            paddle.draw(screen)
            ball.draw(screen)
            for b in blocks:
                b.draw(screen)
            family_member.draw(screen)
            if villain:
                villain.draw(screen)
                
            draw_text(f"SCORE: {score}", font, WHITE, screen, 100, 30)
            draw_text(f"LIVES: {lives}", font, WHITE, screen, WIDTH - 100, 30)
            draw_text(f"LEVEL: {level}", font, WHITE, screen, WIDTH // 2, 30)
            small_font = pygame.font.Font(None, 22)
            draw_text("ESC: PAUSE", small_font, (120, 120, 120), screen, WIDTH - 58, HEIGHT - 15)

            if state == "LEVEL_CLEARED":
                if level < 4:
                    draw_text("LEVEL CLEARED!", large_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//2)
                    draw_text("PRESS SPACE FOR NEXT LEVEL", font, NEON_PINK, screen, WIDTH//2, HEIGHT//2 + 50)
                else:
                    draw_text("YOU WIN!", large_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//2)
            elif state == "GAME_OVER":
                draw_text("GAME OVER", large_font, NEON_RED, screen, WIDTH//2, HEIGHT//2)
                draw_text("PRESS SPACE TO RESTART", font, NEON_PINK, screen, WIDTH//2, HEIGHT//2 + 50)
                hi_font = pygame.font.Font(None, 26)
                entries = load_scores()
                if entries:
                    draw_text(f"BEST: {entries[0][0]}  {entries[0][1]:,}", hi_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//2 + 90)
            elif state == "GAME_WON":
                draw_text("DEMOCRACY SAVED!", large_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//2)
                draw_text("PRESS SPACE TO RESTART", font, NEON_PINK, screen, WIDTH//2, HEIGHT//2 + 50)
                hi_font = pygame.font.Font(None, 26)
                entries = load_scores()
                if entries:
                    draw_text(f"BEST: {entries[0][0]}  {entries[0][1]:,}", hi_font, NEON_BLUE, screen, WIDTH//2, HEIGHT//2 + 90)

        # Pause overlay draws on top of whatever is rendered
        if state == "PAUSED":
            draw_pause_overlay(screen, font, large_font)

        # Initials entry screen
        if state == "ENTER_INITIALS":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            bw, bh = 420, 240
            bx, by = (WIDTH-bw)//2, (HEIGHT-bh)//2
            pygame.draw.rect(screen, (20,30,60), (bx,by,bw,bh), border_radius=12)
            pygame.draw.rect(screen, NEON_PINK, (bx,by,bw,bh), width=2, border_radius=12)
            draw_text("NEW HIGH SCORE!", font, NEON_PINK, screen, WIDTH//2, by+40)
            draw_text(f"{score:,}", large_font, WHITE, screen, WIDTH//2, by+85)
            draw_text("ENTER INITIALS:", font, WHITE, screen, WIDTH//2, by+140)
            # Show typed initials with cursor boxes
            ini_font = pygame.font.Font(None, 72)
            for i in range(3):
                cx = WIDTH//2 - 60 + i*44
                ch = current_initials[i] if i < len(current_initials) else '_'
                clr = WHITE if i < len(current_initials) else (80,80,80)
                draw_text(ch, ini_font, clr, screen, cx, by+185)
            draw_text("A-Z  0-9  !  ?  &     ENTER to confirm", pygame.font.Font(None,22), (140,140,140), screen, WIDTH//2, by+225)

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)

if __name__ == "__main__":
    asyncio.run(main())
