import asyncio
import pygame
import random
import sys
import os
import math

# --- Constants ---
WIDTH = 600
HEIGHT = 800
FPS = 60

# --- Colors ---
WHITE = (250, 250, 250)      # Slightly off-white for sketch paper feel
BLACK = (20, 20, 20)         # Very dark grey for ink
RED = (220, 50, 50)
PAPER_TEXTURE_COLOR = (240, 235, 225)

# --- Initialize Pygame ---
pygame.init()
pygame.mixer.init() # Initialize sound engine
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Truth Evaders")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
serif_font = pygame.font.SysFont('serif', 24)

# --- Asset Dictionaries ---
IMAGES = {}
SOUNDS = {}

def load_assets():
    try:
        IMAGES['pam'] = pygame.image.load("assets/images/pam_bust_pixel.png").convert_alpha()
        # Scale pam slightly down
        IMAGES['pam'] = pygame.transform.scale(IMAGES['pam'], (64, 64))
        IMAGES['ghis'] = pygame.image.load("assets/images/ghis_bust_pixel.png").convert_alpha()
        IMAGES['ghis'] = pygame.transform.scale(IMAGES['ghis'], (64, 64))
    except Exception as e:
        print("Warning: Missing some bust images", e)
        
    # Placeholder for SOUNDS when .wav files are actually provided
    for s_name in ['shot', 'rip', 'march']:
        try:
            SOUNDS[s_name] = pygame.mixer.Sound(f"assets/sounds/{s_name}.wav")
        except:
            pass

def draw_text(text, _font, color, surface, x, y):
    textobj = _font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

class VillainTarget:
    def __init__(self, v_type):
        self.type = v_type # "pam" or "ghis"
        self.width = 64
        self.height = 64
        self.direction = random.choice([-1, 1])
        self.x = -self.width if self.direction == 1 else WIDTH
        self.y = 40
        self.speed = 3
        self.active = True
        self.score_value = 50 if self.type == "pam" else random.choice([100, 200, 300])
        self.phrase = "DOW 50!" if self.type == "pam" else "PARDON ME!"
        self.anim_timer = 0
        self.flap_open = False

    def update(self):
        self.x += self.speed * self.direction
        if (self.direction == 1 and self.x > WIDTH) or (self.direction == -1 and self.x < -self.width):
            self.active = False
            
        self.anim_timer += 1
        if self.anim_timer > 15:
            self.anim_timer = 0
            self.flap_open = not self.flap_open

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if not self.active: return
        tx, ty = int(self.x), int(self.y)
        
        # Determine image
        img = IMAGES.get(self.type)
        if img:
            # Wooden puppet styling - if jaw open, draw base image slightly shifted down
            if self.direction == -1:
                img = pygame.transform.flip(img, True, False)
                
            if self.flap_open:
                # Top half
                surface.blit(img, (tx, ty), (0, 0, self.width, self.height // 2 + 5))
                # Bottom half (jaw) dropped down 4 pixels
                surface.blit(img, (tx, ty + 4), (0, self.height // 2 + 5, self.width, self.height // 2 - 5))
            else:
                surface.blit(img, (tx, ty))
        else:
            pygame.draw.rect(surface, RED, (tx, ty, self.width, self.height))
            
        # Draw speech bubble
        if self.flap_open:
            bubble_x = tx + (self.width if self.direction == 1 else -80)
            bubble_y = ty - 20
            pygame.draw.rect(surface, WHITE, (bubble_x, bubble_y, 80, 20))
            pygame.draw.rect(surface, BLACK, (bubble_x, bubble_y, 80, 20), 2)
            small_f = pygame.font.Font(None, 18)
            t_surface = small_f.render(self.phrase, True, BLACK)
            surface.blit(t_surface, (bubble_x + 5, bubble_y + 4))

def get_sketch_line(x1, y1, x2, y2, jitter=2):
    """Returns a list of points representing a scribbled/jittery line."""
    points = []
    dist = math.hypot(x2 - x1, y2 - y1)
    steps = int(dist / 5)
    if steps == 0: steps = 1
    
    for i in range(steps + 1):
        t = i / steps
        cx = x1 + (x2 - x1) * t
        cy = y1 + (y2 - y1) * t
        jx = cx + random.uniform(-jitter, jitter)
        jy = cy + random.uniform(-jitter, jitter)
        points.append((jx, jy))
    return points

# --- Names Parsing ---
def load_names():
    names = {"top": [], "mid": [], "bot": []}
    try:
        with open("assets/names.md", "r") as f:
            current_section = None
            for line in f:
                line = line.strip()
                if not line: continue
                if line.startswith("# Top Row"):
                    current_section = "top"
                elif line.startswith("# Rows 2-3"):
                    current_section = "mid"
                elif line.startswith("# Rows 4-5"):
                    current_section = "bot"
                elif not line.startswith("#"):
                    if current_section:
                        names[current_section].append(line)
    except Exception as e:
        print("Could not load names.md", e)
        # Fallbacks
        names["top"] = ["Trump"] * 11
        names["mid"] = ["Epstein"] * 22
        names["bot"] = ["Maxwell"] * 22
    return names

# --- Classes ---
class Player:
    def __init__(self):
        self.width = 60
        self.height = 30
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60
        self.speed = 6
        self.color = BLACK
        # Generate sketch geometry for the player once
        self.points_body = [(0, 10), (self.width, 10), (self.width, self.height), (0, self.height), (0, 10)]
        self.points_turret = [(20, 10), (20, 0), (40, 0), (40, 10)]

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        # Draw sketchy tank
        tx, ty = int(self.x), int(self.y)
        for i in range(len(self.points_body)-1):
            p1 = self.points_body[i]
            p2 = self.points_body[i+1]
            pts = get_sketch_line(tx + p1[0], ty + p1[1], tx + p2[0], ty + p2[1])
            if len(pts) > 1: pygame.draw.lines(surface, self.color, False, pts, 2)
            
        for i in range(len(self.points_turret)-1):
            p1 = self.points_turret[i]
            p2 = self.points_turret[i+1]
            pts = get_sketch_line(tx + p1[0], ty + p1[1], tx + p2[0], ty + p2[1])
            if len(pts) > 1: pygame.draw.lines(surface, self.color, False, pts, 2)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 3
        self.active = True

    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.active = False
            
    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius)

class Alien:
    def __init__(self, x, y, name, type_idx):
        self.x = x
        self.y = y
        self.width = 36
        self.height = 24
        self.name = name
        self.type_idx = type_idx
        self.state = "ACTIVE" # ACTIVE, REVEALING
        self.reveal_timer = 0
        self.active = True

        # Pre-calculate scribble points for body
        self.body_lines = []
        if type_idx == 0:
            # Type 1: Spiky
            pts = [(0, self.height), (self.width//2, 0), (self.width, self.height)]
            for i in range(len(pts)-1):
                self.body_lines.append(get_sketch_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))
        elif type_idx == 1:
            # Type 2: Boxy
            pts = [(0,0), (self.width,0), (self.width,self.height), (0,self.height), (0,0)]
            for i in range(len(pts)-1):
                self.body_lines.append(get_sketch_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))
        else:
            # Type 3: Round-ish (Octagon approximate)
            pts = [(10,0),(26,0),(36,10),(36,24),(0,24),(0,10),(10,0)]
            for i in range(len(pts)-1):
                self.body_lines.append(get_sketch_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))

    def hit(self):
        self.state = "REVEALING"
        self.reveal_timer = 60 # Show name for 1 second

    def update(self):
        if self.state == "REVEALING":
            self.reveal_timer -= 1
            if self.reveal_timer <= 0:
                self.active = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if not self.active: return
        tx, ty = int(self.x), int(self.y)
        
        if self.state == "ACTIVE":
            # Draw Sketch Body
            for sketch in self.body_lines:
                shifted = [(p[0]+tx, p[1]+ty) for p in sketch]
                if len(shifted) > 1:
                    pygame.draw.lines(surface, BLACK, False, shifted, 2)
            
            # Draw Redacted Placard (solid black scribble block)
            p_w, p_h = self.width + 4, 12
            pygame.draw.rect(surface, BLACK, (tx - 2, ty + 8, p_w, p_h))
            # Rough edges
            for i in range(3):
                pygame.draw.line(surface, BLACK, (tx-4, ty+8+i*4), (tx+p_w+2, ty+8+i*4), 2)
                
        elif self.state == "REVEALING":
            # Draw morphing placard (white background, black border, text)
            p_w, p_h = self.width + 10, 16
            pygame.draw.rect(surface, WHITE, (tx - 5, ty + 6, p_w, p_h))
            pygame.draw.rect(surface, BLACK, (tx - 5, ty + 6, p_w, p_h), 2)
            
            # Tiny font
            t_surface = serif_font.render(self.name, True, BLACK)
            t_surface = pygame.transform.scale(t_surface, (p_w - 4, p_h - 4))
            surface.blit(t_surface, (tx - 3, ty + 8))


# --- MAIN LOOP ---
async def main():
    load_assets()
    names_db = load_names()
    clock = pygame.time.Clock()
    
    state = "START"
    level = 1
    score = 0
    lives = 3
    
    player = Player()
    bullets = []
    aliens = []
    
    alien_dir = 1
    alien_speed_x = 1.0
    alien_move_timer = 0
    alien_move_threshold = 30
    
    def init_level(lvl):
        nonlocal bullets, player, aliens, alien_dir, alien_speed_x, alien_move_threshold
        bullets.clear()
        player = Player()
        aliens = []
        alien_dir = 1
        alien_speed_x = 1.0 + (lvl * 0.2)
        alien_move_threshold = max(5, 30 - lvl * 2)
        
        # Build Grid (11 cols x 5 rows)
        start_x = 50
        start_y = 100
        pad_x = 42
        pad_y = 36
        
        # Shuffle names for this level
        n_top = random.sample(names_db["top"], min(len(names_db["top"]), 11))
        n_mid = random.sample(names_db["mid"], min(len(names_db["mid"]), 22))
        n_bot = random.sample(names_db["bot"], min(len(names_db["bot"]), 22))
        
        for row in range(5):
            for col in range(11):
                # Determine Name & Type
                if row == 0:
                    name = n_top[col % len(n_top)]
                    typ = 0
                elif row <= 2:
                    idx = ((row-1)*11 + col) % len(n_mid)
                    name = n_mid[idx]
                    typ = 1
                else:
                    idx = ((row-3)*11 + col) % len(n_bot)
                    name = n_bot[idx]
                    typ = 2
                    
                ax = start_x + col * pad_x
                ay = start_y + row * pad_y
                aliens.append(Alien(ax, ay, name, typ))

    init_level(level)
    
    villain = None
    villain_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif state == "START" and event.key == pygame.K_SPACE:
                    state = "PLAYING"
                elif state == "PLAYING" and event.key == pygame.K_SPACE:
                    # Shoot
                    if len(bullets) < 3:
                        bullets.append(Bullet(player.x + player.width // 2, player.y))
                        if 'shot' in SOUNDS: SOUNDS['shot'].play()

        keys = pygame.key.get_pressed()

        if state == "PLAYING":
            player.move(keys)
            
            # Villain logic
            villain_timer += 1
            if villain_timer > 600 and villain is None:
                v_type = "pam" if random.random() < 0.5 else "ghis"
                villain = VillainTarget(v_type)
            
            if villain:
                villain.update()
                if not villain.active:
                    villain = None
                    villain_timer = 0
            
            # Alien movement logic
            alien_move_timer += 1
            shift_down = False
            if alien_move_timer >= alien_move_threshold:
                alien_move_timer = 0
                if 'march' in SOUNDS: SOUNDS['march'].play()
                for a in aliens:
                    if a.state == "ACTIVE":
                        a.x += alien_speed_x * 8 * alien_dir
                
                # Check walls
                for a in aliens:
                    if a.state == "ACTIVE":
                        if a.x > WIDTH - 40 or a.x < 10:
                            shift_down = True
                            break
                            
            if shift_down:
                alien_dir *= -1
                for a in aliens:
                    if a.state == "ACTIVE":
                        a.y += 15
                        a.x += alien_speed_x * 8 * alien_dir # Correct overshoot
            
            for b in bullets:
                b.move()
            bullets = [b for b in bullets if b.active]
            
            # Collisions (Bullets -> Aliens)
            for b in bullets:
                b_rect = pygame.Rect(b.x - b.radius, b.y - b.radius, b.radius*2, b.radius*2)
                
                # Check Villain
                if villain and villain.active and villain.get_rect().colliderect(b_rect):
                    b.active = False
                    villain.active = False
                    score += villain.score_value
                    if 'rip' in SOUNDS: SOUNDS['rip'].play()
                    villain = None
                    villain_timer = 0
                    continue

                # Check Aliens
                for a in aliens:
                    if a.state == "ACTIVE" and a.get_rect().colliderect(b_rect):
                        b.active = False
                        a.hit()
                        score += 10
                        if 'rip' in SOUNDS: SOUNDS['rip'].play()
                        break
                        
            # Update Aliens (revealing to dead)
            for a in aliens:
                a.update()
            
            aliens = [a for a in aliens if a.active]
            
            if len(aliens) == 0:
                level += 1
                init_level(level)

        # Draw
        screen.fill(WHITE)

        if state == "START":
            draw_text("TRUTH EVADERS", large_font, BLACK, screen, WIDTH//2, HEIGHT//3)
            draw_text("PRESS SPACE TO START", font, BLACK, screen, WIDTH//2, HEIGHT//2)
        elif state == "PLAYING":
            player.draw(screen)
            for b in bullets:
                b.draw(screen)
            
            for a in aliens:
                a.draw(screen)
                
            if villain:
                villain.draw(screen)
            
            draw_text(f"SCORE: {score}", font, BLACK, screen, 100, 30)
            draw_text(f"LIVES: {lives}", font, BLACK, screen, WIDTH - 100, 30)
            draw_text(f"LEVEL: {level}", font, BLACK, screen, WIDTH//2, 30)

        pygame.display.flip()
        await asyncio.sleep(0) # IMPORTANT FOR PYGBAG
        clock.tick(FPS)

if __name__ == "__main__":
    asyncio.run(main())
