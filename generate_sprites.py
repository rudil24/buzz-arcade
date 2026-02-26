import os
import io
from PIL import Image, ImageDraw

os.makedirs('python_games/iceout/assets/sprites', exist_ok=True)

# Colors
NEON_BLUE_TRANS = (0, 243, 255, 120)
NEON_BLUE_SOLID = (0, 243, 255, 255)
NEON_PINK = (255, 0, 234, 255)
NEON_PURPLE = (200, 100, 255, 120)
NEON_GREEN = (100, 255, 100, 120)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)
RED = (255, 0, 60, 255)
BROWN = (139, 69, 19, 255)
BLONDE = (255, 215, 0, 255)
SKIN_LIGHT = (255, 204, 153, 255)
SKIN_DARK = (184, 115, 51, 255)

# --- 1. Paddle & Ball (Redrawn for perfection) ---
def make_paddle_and_ball():
    # Paddle (100x20)
    paddle = Image.new('RGBA', (100, 20), TRANSPARENT)
    pdraw = ImageDraw.Draw(paddle)
    pdraw.rectangle([10, 0, 90, 19], fill=NEON_BLUE_SOLID)
    pdraw.pieslice([0, 0, 19, 19], 90, 270, fill=RED)
    pdraw.pieslice([80, 0, 99, 19], -90, 90, fill=RED)
    pdraw.rectangle([10, 2, 90, 17], outline=WHITE, width=1)
    pdraw.line([30, 15, 45, 2], fill=(255, 255, 255, 150), width=2)
    pdraw.line([60, 15, 65, 8], fill=(255, 255, 255, 150), width=2)
    paddle.save('python_games/iceout/assets/sprites/paddle.png')

    # Ball (16x16)
    ball = Image.new('RGBA', (16, 16), TRANSPARENT)
    bdraw = ImageDraw.Draw(ball)
    bdraw.ellipse([0, 0, 15, 15], fill=WHITE, outline=NEON_BLUE_SOLID)
    bdraw.ellipse([2, 2, 13, 13], fill=(200, 250, 255, 255))
    bdraw.ellipse([4, 4, 8, 8], fill=WHITE)
    ball.save('python_games/iceout/assets/sprites/ball.png')

make_paddle_and_ball()

# --- 2. Blocks ---
def make_block(name, color):
    img = Image.new('RGBA', (32, 32), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    draw.rectangle([2, 2, 29, 29], fill=color)
    draw.rectangle([0, 0, 31, 31], outline=WHITE, width=1)
    draw.line([5, 25, 25, 5], fill=(255, 255, 255, 180), width=2)
    img.save(f'python_games/iceout/assets/sprites/{name}.png')

make_block('block_blue', NEON_BLUE_TRANS)
make_block('block_purple', NEON_PURPLE)
make_block('block_green', NEON_GREEN)

# --- 3. The Family Members (Custom Pixel Art) ---
def draw_pixel_person(filename, hair_color, skin_color, shirt_color, pants_color, is_female=False, is_child=False):
    # Base size 12x16 for pixel math, then we scale to 30x40
    base_w, base_h = 12, 16
    img = Image.new('RGBA', (base_w, base_h), TRANSPARENT)
    d = ImageDraw.Draw(img)
    
    # Adjust heights for kids
    head_y = 2 if not is_child else 4
    
    # Hair
    if is_female:
        d.rectangle([3, head_y-1, 8, head_y+5], fill=hair_color) # Long hair flow
    else:
        d.rectangle([3, head_y-1, 8, head_y+1], fill=hair_color) # Short hair

    # Head
    d.rectangle([4, head_y, 7, head_y+3], fill=skin_color)
    # Eyes
    d.point((4, head_y+1), fill=BLACK)
    d.point((6, head_y+1), fill=BLACK)
    
    # Body
    body_y = head_y + 4
    body_h = 4 if not is_child else 3
    d.rectangle([3, body_y, 8, body_y+body_h], fill=shirt_color)
    
    # Legs
    legs_y = body_y + body_h + 1
    d.line([4, legs_y, 4, 14], fill=pants_color)
    d.line([7, legs_y, 7, 14], fill=pants_color)
    
    # Shoes
    d.point((4, 15), fill=BLACK)
    d.point((7, 15), fill=BLACK)
    
    # Arms
    d.line([2, body_y, 2, body_y+2], fill=shirt_color)
    d.line([9, body_y, 9, body_y+2], fill=shirt_color)
    # Hands
    d.point((2, body_y+3), fill=skin_color)
    d.point((9, body_y+3), fill=skin_color)

    # Scale up perfectly
    final_img = img.resize((30, 40), Image.Resampling.NEAREST)
    final_img.save(f'python_games/iceout/assets/sprites/{filename}.png')

# Create the specific family members requested
draw_pixel_person('fam_dad', BROWN, SKIN_DARK, (50, 100, 200, 255), (50, 50, 50, 255))
draw_pixel_person('fam_mom', BLONDE, SKIN_LIGHT, (200, 50, 100, 255), (100, 100, 200, 255), is_female=True)
draw_pixel_person('fam_son', BROWN, SKIN_DARK, (50, 200, 50, 255), (200, 200, 50, 255), is_child=True)
draw_pixel_person('fam_daughter', BLONDE, SKIN_LIGHT, (255, 100, 200, 255), (255, 255, 255, 255), is_female=True, is_child=True)

# --- 4. Hand-Drawn Full Body Pixel Art Villains (24×32, scaled 3× to 72×96) ---
# Each villain has a distinct silhouette and costume at true retro resolution.

colors_map = {
    '.': TRANSPARENT,
    'K': BLACK,
    'W': WHITE,
    # BORTAC Agent (villain1) - camo + tactical gear + black balaclava
    'Z': (75, 83, 32, 255),    # Olive/camo dark green
    'z': (120, 130, 60, 255),  # Camo light green
    'c': (90, 75, 50, 255),    # Camo brown
    'q': (50, 50, 50, 255),    # Black balaclava/facemask
    'e': (200, 200, 200, 255), # Glasses frames (light grey)
    'j': (130, 130, 130, 255), # Glasses lens tint
    'v': (180, 140, 80, 255),  # Tan helmet strap/trim
    'n': (60, 60, 60, 255),    # Dark tactical vest panel
    'p': (255, 220, 100, 255), # Gold "POLICE BORTAC" badge text
    'x': (30, 30, 30, 255),    # Black gloves
    # General / Trench Coat (villain2)
    'g': (50, 70, 30, 255),    # Olive trench coat dark
    'G': (75, 100, 45, 255),   # Olive trench coat mid
    'f': (200, 170, 50, 255),  # Gold buttons / rank stars
    'h': (20, 20, 60, 255),    # Dark navy uniform under coat
    'S': SKIN_LIGHT,
    # ICE Agent Woman (villain3)
    'b': (50, 80, 140, 255),   # Blue cap / navy jacket
    'B': (35, 55, 110, 255),   # Dark navy
    'k': (90, 100, 80, 255),   # Olive tactical vest
    'y': (220, 180, 80, 255),  # Gold "ICE" badge letters
    'w': (200, 60, 60, 255),   # Red nails accent
    'l': (160, 110, 70, 255),  # Light brown hair
    # Trump (villain4)
    'Y': (255, 215, 0, 255),   # Yellow hair
    'O': (255, 155, 80, 255),  # Orange skin
    'N': (25, 25, 112, 255),   # Navy suit
    'R': (200, 20, 40, 255),   # Red tie
    'H': (245, 245, 245, 255), # White shirt
    'D': (10, 10, 70, 255),    # Dark navy pants
}

# ------------------------------------------------------------------
# Villain 1: BORTAC Agent — tactical helmet, black balaclava/facemask,
#            camo uniform, tactical chest rig, glasses.
# Grid: 24 wide × 32 tall
# ------------------------------------------------------------------
villain1_grid = [
    # Row  0-3: Tactical helmet
    "........vvvvvvvv........",
    ".......vZZZZZZZZv.......",
    "......vZZZZZZZZZZv......",
    "......ZZZZZZZZZZZZ......",
    # Row  4-7: Head with glasses + balaclava
    "......ZqqqqqqqqqqZ......",  # top of balaclava
    ".....Zqeejjjjeeqq.......",  # glasses band
    ".....Zqejjjjjjeqq.......",  # glasses lenses
    ".....Zqqqqqqqqqq........",  # balaclava nose/mouth area
    # Row  8-9: Neck + collar
    ".......qqqqqqqq.........",
    ".......nnnnnnnn.........",
    # Row 10-15: Chest rig / tactical vest over camo
    "......nnnnnnnnnn........",
    ".....nncZcZcZcnn........",  # camo pattern on vest
    "....pppnnnnnnnppp.......",  # POLICE badge row
    "....nnnnnnnnnnnnn.......",
    "...cZcnnnnnnnnncZc......",
    "...ZcZnnnnnnnnnZcZ......",
    # Row 16-19: Arms + waist
    "..xxncZcZcZcZcZcnxx.....",  # gloved arms out + camo torso
    "..xxZZZZZZZZZZZZZxx.....",
    "...KKZcZcZcZcZcZKK......",  # belt line
    "...KKZZcZcZcZcZZKK......",
    # Row 20-25: Hips / camo pants
    ".....ZZZZcZcZZZZ........",
    ".....cZZZZZZZZZc........",
    ".....ZcZZccZZZcZ........",
    ".....ZZcZZZZcZZZ........",
    ".....ZcZcZZcZcZZ........",
    ".....ZZcZcZcZcZZ........",
    # Row 26-29: Lower legs
    "......ZcZZ.ZZcZ.........",
    "......ZZcZ.ZcZZ.........",
    "......ZcZZ.ZZcZ.........",
    "......ZZcZ.ZcZZ.........",
    # Row 30-31: Boots
    ".....xZZZZ.ZZZZx........",
    ".....xxxxK.Kxxxx........",
]

# ------------------------------------------------------------------
# Villain 2: General in Olive Trench Coat — gold buttons, rank stars,
#            dark navy uniform underneath, grey/white hair.
# Grid: 24 wide × 32 tall
# ------------------------------------------------------------------
villain2_grid = [
    # Hair + head
    "........WWWWWWWW........",
    ".......WSSSSSSSW........",
    "......WSSSSSSSSW........",
    ".......SSEEESSS.........",
    ".......SSSSSSS..........",
    # Collar / scarf area
    ".......hSSSSSh..........",
    ".......hhhhhhhh.........",
    # Shoulders + coat open (wide)
    "......GGGhhhGGG.........",
    ".....GGGGGhGGGGG........",
    "....gGfGGGhGGGfGg.......",  # gold buttons on each side
    "....gGGGGGhGGGGGg.......",
    "....gGfGGGhGGGfGg.......",
    "....gGGGGGhGGGGGg.......",
    # Arms wide — coat draping
    "...ggGGGGGhGGGGGgg......",
    "...ggGGGGGhGGGGGgg......",
    "....gGfGGGhGGGfGg.......",
    "....gGGGGGhGGGGGg.......",
    "....gGfGGGhGGGfGg.......",
    "....gGGGGGhGGGGGg.......",
    # Lower coat — longer trench
    ".....GGGGGhGGGGG........",
    ".....GGGGGhGGGGG........",
    ".....GGGGGhGGGGG........",
    ".....GGGGGhGGGGG........",
    ".....GGGGGhGGGGG........",
    # Hem split
    ".....gGGG...GGGg........",
    ".....hhhh...hhhh........",
    # Trouser legs visible below hem
    "......hhh...hhh.........",
    "......hhh...hhh.........",
    "......hhh...hhh.........",
    "......hhh...hhh.........",
    "......KKK...KKK.........",
    ".......KK...KK..........",
]

# ------------------------------------------------------------------
# Villain 3: ICE Agent Woman — blue cap, long brown hair, tactical vest
#            with "ICE" badge, navy jacket, jeans.
# Grid: 24 wide × 32 tall
# ------------------------------------------------------------------
villain3_grid = [
    # Cap brim + dome
    "......bbbbbbbbb.........",
    ".....bbbbbbbbbbb........",
    ".....BBBBBBBBBBB........",
    "......bbbbbbbbb.........",
    # Hair flowing out from sides of cap
    ".....lbSSSSSSSbl........",
    "....llbSSESSSEbl........",  # eyes
    "....llbSSSoSSSbl........",  # 'o' = mouth (reuse 'O' not in map, use black K)
    "....llllSSSSSSll........",
    # Neck
    ".....lllSSSSSSl.........",
    ".......lSSSSSl..........",
    # Chest — tactical vest over dark jacket
    "......BkkkkkkkB.........",
    ".....BBkyyyykBBB........",  # gold ICE letters
    ".....BBkkkkkkkBB........",
    "....BBBkkkkkkBBBB.......",
    # Arms out
    "...BBBBBkkkkBBBBBB......",
    "...BBBBBkkkkBBBBBB......",
    "...xxBBBkkkkBBBxxB......",  # gloved hands at waist
    "...xxBBBBBBBBBxxB.......",
    # Waist / belt
    ".....BBBBkBBBBB.........",
    # Jeans / trousers
    ".....bbbbbbbbbbb........",  # reuse b color as denim blue
    ".....bbbbbbbbbbb........",
    ".....bbbb.bbbbb.........",
    ".....bbbb.bbbbb.........",
    ".....bbbb.bbbbb.........",
    ".....bbbb.bbbbb.........",
    ".....bbbb.bbbbb.........",
    ".....bbbb.bbbbb.........",
    # Lower leg + shoe
    ".....Bbbb.bbbbB.........",
    ".....Bbbb.bbbbB.........",
    ".....KBBB.BBBK..........",
    "......KKK.KKK...........",
    ".......KK.KK............",
]
# fix mouth row — use K for dot
villain3_grid[6] = "....llbSSSKSSSbl........"

# ------------------------------------------------------------------
# Villain 4: Trump — swept yellow hair, orange skin, navy suit, red tie,
#            white shirt, dark pants, pointing finger.
# Grid: 24 wide × 32 tall
# ------------------------------------------------------------------
villain4_grid = [
    # Hair swept back/over, wide
    "......YYYYYYYY..........",
    ".....YYYYOOYYY..........",
    "....YYYOOOEOOY..........",  # E = eye
    ".....YOOOOOOOY..........",
    "......OOOOOOOY..........",
    # Chin / neck barely visible
    ".......OOOOOOO..........",
    "........OO.....NNNNN....",  # White shirt collar + suit shoulder
    # Shoulders wide
    "......NNORHNN..........",   # R = Red tie, H = shirt
    ".....NNNORHNNN..........",
    "....NNNNORHNNN..........",  # lapel
    "....NNNNORHNNN..........",
    # Body, one arm out pointing (right = viewer's left)
    "...DDDNNORHNNNNN........",  # D arm out
    "...DDDNNORhNNNNN........",
    "....OODNORhNNNNN........",  # hand (O = orange skin)
    "....OODNORhNNNNN........",
    # Belt / hips
    "......NNNRNNNNNN........",
    "......DDDDDDDDD.........",
    "......DDDDDDDDD.........",
    "......DDDDDDDDD.........",
    "......DDDDDDDDD.........",
    # Trouser break
    "......DDD.DDDDD.........",
    "......DDD.DDDDD.........",
    "......DDD.DDDDD.........",
    "......DDD.DDDDD.........",
    "......DDD.DDDDD.........",
    "......DDD.DDDDD.........",
    "......DDD.DDDDD.........",
    # Shoes
    "......DDD.DDDDD.........",
    ".....KDDD.DDDDK.........",
    ".....KKKK.KKKKK.........",
    "......KKK.KKK...........",
    ".......KK.KK............",
]


def draw_grid_sprite(filename, grid):
    h = len(grid)
    w = max(len(row) for row in grid)
    img = Image.new('RGBA', (w, h), TRANSPARENT)
    pixels = img.load()

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            color = colors_map.get(char, BLACK if char == 'E' else TRANSPARENT)
            pixels[x, y] = color

    # Scale 3× with nearest-neighbor for crisp pixel art
    scaled_img = img.resize((w * 3, h * 3), Image.Resampling.NEAREST)
    scaled_img.save(f'python_games/iceout/assets/sprites/{filename}.png')
    print(f"Generated {filename}.png  ({w}×{h} → {w*3}×{h*3})")


draw_grid_sprite('villain1', villain1_grid)
draw_grid_sprite('villain2', villain2_grid)
draw_grid_sprite('villain3', villain3_grid)
draw_grid_sprite('villain4', villain4_grid)

print("All villain sprites generated!")
