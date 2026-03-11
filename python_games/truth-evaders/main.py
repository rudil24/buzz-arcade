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

WHITE = (250, 250, 250)
BLACK = (20, 20, 20)
GREY = (160, 160, 160)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
PAPER_TEXTURE_COLOR = (240, 235, 225)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Truth Evaders")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
# Bold font for the names (rendered natively)
name_font = pygame.font.Font(None, 18)
name_font.set_bold(True)

# --- Asset Dictionaries ---
IMAGES = {}
SOUNDS = {}

def load_assets():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        IMAGES['pam'] = pygame.image.load(os.path.join(BASE_DIR, "assets/images/pam_bust_pixel.png")).convert_alpha()
        IMAGES['pam'] = pygame.transform.scale(IMAGES['pam'], (64, 64))
        IMAGES['ghis'] = pygame.image.load(os.path.join(BASE_DIR, "assets/images/ghis_bust_pixel.png")).convert_alpha()
        IMAGES['ghis'] = pygame.transform.scale(IMAGES['ghis'], (64, 64))
    except Exception as e:
        print("Warning: Missing some bust images", e)
        
    for s_name in ['shot', 'rip', 'march', 'pam', 'ghis', 'boss_hit']:
        try:
            SOUNDS[s_name] = pygame.mixer.Sound(os.path.join(BASE_DIR, f"assets/sounds/{s_name}.wav"))
        except:
            pass

def draw_text(text, _font, color, surface, x, y):
    textobj = _font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

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
    pygame.draw.rect(surface, BLUE, (bx, by, bw, bh), width=2, border_radius=12)
    draw_text("BACK TO CONCOURSE?", font, WHITE, surface, WIDTH//2, by + 45)
    # ESC row
    esc_font = pygame.font.Font(None, 28)
    draw_text("ESC  ·  QUIT", esc_font, RED, surface, WIDTH//2, by + 100)
    # Spacebar icon + CONTINUE
    draw_spacebar_icon(surface, WIDTH//2 - 60, by + 148)
    draw_text("CONTINUE", esc_font, BLUE, surface, WIDTH//2 + 30, by + 148)

class VillainTarget:
    def __init__(self, v_type):
        self.type = v_type # "pam" or "ghis"
        self.width = 64
        self.height = 64
        self.direction = random.choice([-1, 1])
        self.x = -self.width if self.direction == 1 else WIDTH
        self.y = 80 # Move down so it doesn't clip top score text
        self.speed = 3
        self.active = True
        self.score_value = 50 if self.type == "pam" else random.choice([100, 200, 300])
        self.phrase = "DOW 50!" if self.type == "pam" else "PARDON ME!"
        if self.type in SOUNDS: SOUNDS[self.type].play()
        self.anim_timer = 0
        self.voice_timer = 0
        self.flap_open = False

    def update(self):
        self.x += self.speed * self.direction
        if (self.direction == 1 and self.x > WIDTH) or (self.direction == -1 and self.x < -self.width):
            self.active = False
            
        self.anim_timer += 1
        if self.anim_timer > 30:
            self.anim_timer = 0
            
        self.voice_timer += 1
        if self.voice_timer >= 120:  # Re-play sound every ~2 seconds
            if self.type in SOUNDS: SOUNDS[self.type].play()
            self.voice_timer = 0
            self.flap_open = not self.flap_open

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if not self.active: return
        tx, ty = int(self.x), int(self.y)
        
        img = IMAGES.get(self.type)
        if img:
            if self.direction == -1:
                img = pygame.transform.flip(img, True, False)
                
            # Bobbing animation instead of shrinking slice
            anim_y = ty + (4 if self.flap_open else 0)
            surface.blit(img, (tx, anim_y))
        else:
            pygame.draw.rect(surface, RED, (tx, ty, self.width, self.height))
            
        if self.flap_open:
            bubble_x = tx + (self.width if self.direction == 1 else -80)
            bubble_y = ty - 25
            pygame.draw.rect(surface, WHITE, (bubble_x, bubble_y, 80, 20))
            pygame.draw.rect(surface, BLACK, (bubble_x, bubble_y, 80, 20), 2)
            small_f = pygame.font.Font(None, 18)
            t_surface = small_f.render(self.phrase, True, BLACK)
            t_rect = t_surface.get_rect(center=(bubble_x + 40, bubble_y + 10))
            surface.blit(t_surface, t_rect)

# --- Names Parsing ---
def load_names():
    names = {"top": [], "mid": [], "bot": []}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(BASE_DIR, "assets/names.md"), "r") as f:
            current_section = ""
            for line in f:
                line = line.strip()
                if not line: continue
                # Match user's md headings accurately
                if "Top Row" in line and line.startswith("#"):
                    current_section = "top"
                elif "Rows 2-3" in line and line.startswith("#"):
                    current_section = "mid"
                elif "Rows 4-5" in line and line.startswith("#"):
                    current_section = "bot"
                elif not line.startswith("#"):
                    if current_section in names:
                        names[current_section].append(line)
    except Exception as e:
        print("Could not load names.md", e)
        names["top"] = ["Trump"] * 11
        names["mid"] = ["Epstein"] * 22
        names["bot"] = ["Maxwell"] * 22
        
    # Prevent empty arrays just in case parsing has odd lines
    if not names["top"]: names["top"] = ["Trump"]
    if not names["mid"]: names["mid"] = ["Epstein"]
    if not names["bot"]: names["bot"] = ["Maxwell"]
    return names

# --- SPACE INVADERS ALIEN SPRITES ---
ALIEN_SPRITES = {
    0: [ # Top row (Squid) - 8x8
        "00011000",
        "00111100",
        "01111110",
        "11011011",
        "11111111",
        "00100100",
        "01011010",
        "10100101"
    ],
    1: [ # Middle rows (Crab) - 11x8
        "00100000100",
        "00010001000",
        "00111111100",
        "01101110110",
        "11111111111",
        "10111111101",
        "10100000101",
        "00011011000"
    ],
    2: [ # Bottom rows (Octopus) - 12x8
        "000011110000",
        "011111111110",
        "111111111111",
        "111001100111",
        "111111111111",
        "000110011000",
        "001101101100",
        "110000000011"
    ]
}

# --- Classes ---
class BaseBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 12
        self.active = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))

class AlienBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 4
        self.height = 12
        self.active = True

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.active = False
            
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
            
    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.get_rect())

class Player:
    def __init__(self):
        self.pixel_size = 5
        self.sprite_map = [
            "   B   ",
            "  BBB  ",
            "  WWW  ",
            " RRRRR ",
            "RRRRRRR",
            "RRRRRRR",
            "RR   RR"
        ]
        self.width = len(self.sprite_map[0]) * self.pixel_size
        self.height = len(self.sprite_map) * self.pixel_size
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60 - self.height
        self.speed = 6

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        tx, ty = int(self.x), int(self.y)
        for row_idx, row_str in enumerate(self.sprite_map):
            for col_idx, char in enumerate(row_str):
                color = None
                if char == 'R': color = RED
                elif char == 'W': color = WHITE
                elif char == 'B': color = BLUE
                
                if color:
                    px = tx + col_idx * self.pixel_size
                    py = ty + row_idx * self.pixel_size
                    pygame.draw.rect(surface, color, (px, py, self.pixel_size, self.pixel_size))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 3
        self.active = True

    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius*2, self.radius*2)

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
        self.state = "ACTIVE"
        self.active = True
        self.sprite_map = ALIEN_SPRITES[type_idx]
        self.pixel_size = 3

    def hit(self):
        self.state = "REVEALED"

    def update(self):
        pass

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        if not self.active: return
        tx, ty = int(self.x), int(self.y)
        
        if self.state == "ACTIVE":
            w_offset = (self.width - (len(self.sprite_map[0]) * self.pixel_size)) // 2
            h_offset = (self.height - (len(self.sprite_map) * self.pixel_size)) // 2
            for row_idx, row_str in enumerate(self.sprite_map):
                for col_idx, char in enumerate(row_str):
                    if char == '1':
                        px = tx + w_offset + col_idx * self.pixel_size
                        py = ty + h_offset + row_idx * self.pixel_size
                        pygame.draw.rect(surface, GREY, (px, py, self.pixel_size, self.pixel_size))
            
            p_w, p_h = self.width + 4, 10
            placard_y = ty + (self.height // 2) - (p_h // 2)
            pygame.draw.rect(surface, BLACK, (tx - 2, placard_y, p_w, p_h))
            for i in range(3):
                pygame.draw.line(surface, BLACK, (tx-4, placard_y+i*3), (tx+p_w+2, placard_y+i*3), 2)
                
        elif self.state == "REVEALED":
            t_surface = name_font.render(self.name, True, (0, 0, 0))
            t_w, t_h = t_surface.get_size()
            
            p_w, p_h = max(self.width, t_w + 6), t_h + 4
            placard_y = ty + (self.height // 2) - (p_h // 2)
            
            placard_surf = pygame.Surface((p_w, p_h), pygame.SRCALPHA)
            pygame.draw.rect(placard_surf, (255, 255, 255, 180), (0, 0, p_w, p_h)) 
            pygame.draw.rect(placard_surf, (20, 20, 20, 180), (0, 0, p_w, p_h), 1)
            
            t_rect = t_surface.get_rect(center=(p_w//2, p_h//2))
            placard_surf.blit(t_surface, t_rect)
            
            # Center the tag over the alien's position
            surface.blit(placard_surf, (tx + self.width//2 - p_w//2, placard_y))


# --- MAIN LOOP ---
SCORES_FILE = "truth-evaders-scores.txt"
ALLOWED_INITIALS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?&')

def load_scores():
    entries = []
    # Attempt WebAssembly localStorage first
    try:
        import platform
        import json
        data = platform.window.localStorage.getItem('truth_evaders_scores')
        if data:
            parsed = json.loads(data)
            # Ensure proper format: [[initials, score], ...]
            return [[str(x[0]), int(x[1])] for x in parsed]
    except Exception:
        pass

    # Fallback to flat file
    try:
        with open(SCORES_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if ',' in line:
                    parts = line.split(',', 1)
                    try:
                        entries.append([parts[0], int(parts[1])])
                    except ValueError:
                        pass
                elif line.isdigit():
                    entries.append(['???', int(line)])
    except Exception:
        pass
    return sorted(entries, key=lambda x: x[1], reverse=True)[:10]

def is_top_10(score):
    scores = load_scores()
    return len(scores) < 10 or score > scores[-1][1]

def save_entry(initials, score):
    entries = load_scores()
    # Tuples become lists in JSON, so standardizing on lists
    entries.append([initials[:3].upper(), score])
    entries = sorted(entries, key=lambda x: x[1], reverse=True)[:10]
    
    # Attempt WebAssembly localStorage format override
    try:
        import platform
        import json
        platform.window.localStorage.setItem('truth_evaders_scores', json.dumps(entries))
    except Exception:
        pass

    try:
        with open(SCORES_FILE, 'w') as f:
            for ini, s in entries:
                f.write(f"{ini},{s}\n")
    except Exception as e:
        print("Could not save score:", e)

def handle_initials_input(event, current_initials, score):
    if event.key == pygame.K_BACKSPACE:
        return current_initials[:-1], False
        
    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
        if len(current_initials) > 0:
            try:
                save_entry(current_initials.ljust(3, '_')[:3], score)
            except Exception:
                pass
            return current_initials, True
            
    elif event.key == pygame.K_ESCAPE:
        if len(current_initials) > 0:
            try:
                save_entry(current_initials.ljust(3, '_')[:3], score)
            except Exception:
                pass
            return current_initials, True
            
    else:
        ch = pygame.key.name(event.key).upper()
        if len(ch) == 1 and ch in ALLOWED_INITIALS and len(current_initials) < 3:
            return current_initials + ch, False
            
    return current_initials, False

async def main():
    load_assets()
    names_db = load_names()
    clock = pygame.time.Clock()
    
    state = "START"
    level = 1
    score = 0
    lives = 3
    delay_timer = 0
    
    player = Player()
    bullets = []
    alien_bullets = []
    aliens = []
    bases = []
    
    alien_dir = 1
    alien_speed_x = 1.0
    alien_move_timer = 0
    alien_move_threshold = 30
    
    def init_level(lvl, reset_player=False):
        nonlocal bullets, alien_bullets, player, aliens, bases, alien_dir, alien_speed_x, alien_move_threshold, villain_targets
        bullets.clear()
        alien_bullets.clear()
        villain_targets.clear() # Clear villain targets on new level
        
        if not reset_player:
            player = Player()
            aliens = []
            alien_dir = 1
            alien_speed_x = 1.0 + (lvl * 0.2)
            alien_move_threshold = max(5, 30 - lvl * 2)
            
            # Build Grid (11 cols x 5 rows)
            start_x = 50
            start_y = 150 # Move down beyond villain lane
            pad_x = 44 # slightly wider separation
            pad_y = 50
            
            n_top = random.sample(names_db["top"], min(len(names_db["top"]), 11))
            n_mid = random.sample(names_db["mid"], min(len(names_db["mid"]), 22))
            n_bot = random.sample(names_db["bot"], min(len(names_db["bot"]), 22))
            
            for row in range(5):
                for col in range(11):
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

            # Build 4 Bases
            bases.clear()
            bw, bh = 12, 12
            for bx in range(4):
                base_x = 75 + bx * 120
                base_y = HEIGHT - 200
                # shape: 6 cols, 5 rows
                for r in range(5):
                    for c in range(6):
                        # cutout bottom center
                        if r >= 3 and 1 <= c <= 4: continue
                        # cutout top corners
                        if r == 0 and (c == 0 or c == 5): continue
                        bases.append(BaseBlock(base_x + c * bw, base_y + r * bh))
        else:
            player.x = WIDTH // 2 - player.width // 2
            # Lift aliens up to 150px away from bases to prevent immediate re-breach
            active_aliens = [al for al in aliens if al.state == "ACTIVE"]
            if active_aliens:
                min_y = min(al.y for al in active_aliens)
                lift_amount = min(150, max(0, min_y - 150))
                for a in aliens:
                    a.y -= lift_amount

    villain_targets = [] # Changed from singular 'villain' to plural list
    villain_timer = 0
    current_initials = ""

    init_level(level)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    import platform
                    platform.window.parent.postMessage('returnToConcourse', '*')
                except Exception:
                    pass
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if state == "ENTER_INITIALS":
                    current_initials, confirm = handle_initials_input(event, current_initials, score)
                    if confirm:
                        level = 1
                        score = 0
                        lives = 3
                        init_level(level)
                        state = "START"
                elif state == "PLAYING" and event.key == pygame.K_ESCAPE:
                    state = "PAUSED"
                elif state == "PAUSED":
                    if event.key == pygame.K_SPACE:
                        state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        try:
                            import platform
                            platform.window.parent.postMessage('returnToConcourse', '*')
                        except Exception:
                            pass
                        sys.exit()
                elif state == "START" and event.key == pygame.K_SPACE:
                    state = "PLAYING"
                elif state == "GAME_OVER" and event.key == pygame.K_SPACE:
                    level = 1
                    score = 0
                    lives = 3
                    init_level(level)
                    state = "PLAYING"
                elif state == "PLAYING" and event.key == pygame.K_SPACE:
                    if len(bullets) < 1: # One bullet at a time constraint
                        bullets.append(Bullet(player.x + player.width // 2, player.y))
                        if 'shot' in SOUNDS: SOUNDS['shot'].play()

        keys = pygame.key.get_pressed()

        if state in ("LIFE_LOST", "LEVEL_CLEAR"):
            delay_timer -= 1
            if delay_timer <= 0:
                if state == "LIFE_LOST":
                    if lives <= 0:
                        if is_top_10(score):
                            state = "ENTER_INITIALS"
                            current_initials = ""
                        else:
                            state = "GAME_OVER"
                    else:
                        init_level(level, reset_player=True)
                        state = "PLAYING"
                elif state == "LEVEL_CLEAR":
                    level += 1
                    init_level(level)
                    state = "PLAYING"

        if state == "PLAYING":
            player.move(keys)
            
            if not villain_targets:
                villain_timer += 1
                if villain_timer > 600:
                    v_type = "pam" if random.random() < 0.5 else "ghis"
                    villain_targets.append(VillainTarget(v_type))
            else:
                villain_timer = 0
            
            for vt in villain_targets:
                vt.update()
            villain_targets = [vt for vt in villain_targets if vt.active] # Filter inactive
            
            alien_move_timer += 1
            shift_down = False
            
            active_aliens = [a for a in aliens if a.state == "ACTIVE"]
            
            if alien_move_timer >= alien_move_threshold:
                alien_move_timer = 0
                if 'march' in SOUNDS: SOUNDS['march'].play()
                for a in aliens:
                    a.x += alien_speed_x * 8 * alien_dir
                
                for a in aliens:
                    if a.x > WIDTH - 40 or a.x < 10:
                        shift_down = True
                        break
                            
            if shift_down:
                alien_dir *= -1
                for a in aliens:
                    a.y += 15
                    a.x += alien_speed_x * 8 * alien_dir 

            # Alien shooting logic
            alien_shoot_chance = min(0.04, 0.005 + level * 0.005)
            if active_aliens and random.random() < alien_shoot_chance:
                shooter = random.choice(active_aliens)
                alien_bullets.append(AlienBullet(shooter.x + shooter.width//2, shooter.y + shooter.height))
            
            for b in bullets: b.move()
            for ab in alien_bullets: ab.move()
            
            bullets = [b for b in bullets if b.active]
            alien_bullets = [ab for ab in alien_bullets if ab.active]
            bases = [b for b in bases if b.active]
            
            # --- collisions ---
            for b in bullets:
                b_rect = b.get_rect()
                
                hit_villain = False
                for vt in villain_targets:
                    if vt.active and b_rect.colliderect(vt.get_rect()):
                        vt.active = False
                        b.active = False
                        score += vt.score_value
                        if 'boss_hit' in SOUNDS: SOUNDS['boss_hit'].play()
                        hit_villain = True
                        break
                if hit_villain:
                    continue

                for a in aliens:
                    if a.state == "ACTIVE" and a.get_rect().colliderect(b_rect):
                        b.active = False
                        a.hit()
                        score += 10
                        if 'rip' in SOUNDS: SOUNDS['rip'].play()
                        break
                        
            for b in bullets:
                if b.active:
                    br = b.get_rect()
                    for base in bases:
                        if base.active and base.get_rect().colliderect(br):
                            base.active = False
                            b.active = False
                            break
                            
            for ab in alien_bullets:
                if ab.active:
                    abr = ab.get_rect()
                    for base in bases:
                        if base.active and base.get_rect().colliderect(abr):
                            base.active = False
                            ab.active = False
                            break
                            
            p_rect = player.get_rect()
            for ab in alien_bullets:
                if ab.active and ab.get_rect().colliderect(p_rect):
                    ab.active = False
                    lives -= 1
                    if 'rip' in SOUNDS: SOUNDS['rip'].play()
                    state = "LIFE_LOST"
                    delay_timer = FPS * 2
            
            breach = False
            for a in aliens:
                if a.state == "ACTIVE":
                    ar = a.get_rect()
                    
                    for base in bases:
                        if base.active and base.get_rect().colliderect(ar):
                            breach = True
                            
                    if ar.colliderect(p_rect) or a.y > HEIGHT - 50:
                        breach = True
                        
                    if breach: break
            
            if breach:
                lives -= 1
                if 'rip' in SOUNDS: SOUNDS['rip'].play()
                state = "LIFE_LOST"
                delay_timer = FPS * 2

            for a in aliens:
                a.update()
            
            import builtins
            if not builtins.any(a.state == "ACTIVE" for a in aliens):
                state = "LEVEL_CLEAR"
                delay_timer = FPS * 2

        screen.fill(WHITE)

        if state == "START":
            draw_text("TRUTH EVADERS", large_font, BLACK, screen, WIDTH//2, HEIGHT//3)
            draw_text("PRESS SPACE TO START", font, BLACK, screen, WIDTH//2, HEIGHT//2)
            entries = load_scores()
            if entries:
                draw_text("HIGH SCORES", font, BLUE, screen, WIDTH//2, HEIGHT//2 + 50)
                hi_font = pygame.font.Font(None, 24)
                for i, s in enumerate(entries[:5]):
                    draw_text(f"{i+1}. {s[0]} {s[1]:,}", hi_font, (100,100,100), screen, WIDTH//2, HEIGHT//2 + 80 + (i*25))
        elif state == "GAME_OVER":
            draw_text("GAME OVER", large_font, RED, screen, WIDTH//2, HEIGHT//3)
            draw_text(f"FINAL SCORE: {score}", font, BLACK, screen, WIDTH//2, HEIGHT//2)
            draw_text("PRESS SPACE TO RESTART", font, BLACK, screen, WIDTH//2, HEIGHT//2 + 50)
        elif state == "LIFE_LOST":
            draw_text("CASUALTY REGISTERED", large_font, RED, screen, WIDTH//2, HEIGHT//3)
        elif state == "LEVEL_CLEAR":
            draw_text("PERPS EXPOSED", large_font, BLUE, screen, WIDTH//2, HEIGHT//3)
            draw_text(f"Get Ready for Level {level + 1}", font, BLACK, screen, WIDTH//2, HEIGHT//2)
        elif state == "PLAYING" or state == "PAUSED":
            player.draw(screen)
            for b in bullets: b.draw(screen)
            for ab in alien_bullets: ab.draw(screen)
            for base in bases: base.draw(screen)
            
            import builtins
            for a in builtins.sorted(aliens, key=lambda al: 0 if al.state=="ACTIVE" else 1):
                a.draw(screen)
                
            for vt in villain_targets:
                vt.draw(screen)
            
            draw_text(f"SCORE: {score}", font, BLACK, screen, 100, 30)
            draw_text(f"LIVES: {lives}", font, BLACK, screen, WIDTH - 100, 30)
            draw_text(f"LEVEL: {level}", font, BLACK, screen, WIDTH//2, 30)

        if state == "ENTER_INITIALS":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            screen.blit(overlay, (0, 0))
            bw, bh = 420, 240
            bx, by = (WIDTH-bw)//2, (HEIGHT-bh)//2
            pygame.draw.rect(screen, WHITE, (bx,by,bw,bh), border_radius=12)
            pygame.draw.rect(screen, BLACK, (bx,by,bw,bh), width=4, border_radius=12)
            draw_text("NEW HIGH SCORE!", large_font, BLACK, screen, WIDTH//2, by+40)
            draw_text(f"{score:,}", large_font, BLUE, screen, WIDTH//2, by+85)
            draw_text("ENTER INITIALS:", font, BLACK, screen, WIDTH//2, by+140)
            
            ini_font = pygame.font.Font(None, 72)
            for i in range(3):
                cx = WIDTH//2 - 60 + i*44
                ch = current_initials[i] if i < len(current_initials) else '_'
                clr = BLACK if i < len(current_initials) else (150,150,150)
                draw_text(ch, ini_font, clr, screen, cx, by+185)
            draw_text("A-Z  0-9  !  ?  &     ENTER to confirm", pygame.font.Font(None,22), (100,100,100), screen, WIDTH//2, by+225)

        if state == "PAUSED":
            draw_pause_overlay(screen, font, large_font)

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)

if __name__ == "__main__":
    asyncio.run(main())
