import zipfile
import os
import shutil
from pathlib import Path

# Fix relative execution paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, 'build', 'web')

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# Remove old files
try: os.remove(os.path.join(TARGET_DIR, 'iceout.apk'))
except OSError: pass
try: os.remove(os.path.join(TARGET_DIR, 'iceout.zip'))
except OSError: pass

os.chdir(BASE_DIR)

with zipfile.ZipFile(os.path.join(TARGET_DIR, 'iceout.apk'), 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('main.py', 'main.py')
    for root, dirs, files in os.walk('assets'):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path)

shutil.copytree('build/web', '/Users/rudil24/Documents/webdev/buzz-arcade/public/games/iceout/', dirs_exist_ok=True)
print("Apk built and copied.")
