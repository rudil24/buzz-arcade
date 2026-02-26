import os
from PIL import Image

img = Image.open('docs/assets/ice_out_game_mockup_1772065213721.png')

# Create output directory
os.makedirs('python_games/iceout/assets/sprites', exist_ok=True)

# Define crops (left, upper, right, lower)
crops = {
    'title.png': (160, 95, 480, 160),
    'block_blue.png': (130, 203, 163, 227),
    'block_purple.png': (170, 203, 201, 227),
    'block_green.png': (430, 203, 461, 227),
    'family.png': (290, 310, 332, 390),
    'villain.png': (215, 420, 290, 480),
    'ball.png': (326, 532, 344, 550),
    'paddle.png': (265, 560, 360, 580)
}

grid = img.copy()

for name, box in crops.items():
    sprite = img.crop(box)
    
    # Simple color keying (removing exact dark blue background)
    # Background color seems to be around rgb(5, 15, 65) or similar.
    # We will do a simple pass to make anything close to dark blue transparent.
    sprite = sprite.convert("RGBA")
    data = sprite.getdata()
    new_data = []
    for item in data:
        # Check if color is dark blue-ish
        if item[0] < 50 and item[1] < 50 and item[2] < 120 and item[0] + item[1] + item[2] < 150:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    sprite.putdata(new_data)
    
    sprite.save(f'python_games/iceout/assets/sprites/{name}')
    print(f"Saved {name}")

print("Extraction complete.")
