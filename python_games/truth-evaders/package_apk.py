import zipfile
import os
import shutil

TARGET_DIR = '/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders/build/web'
os.makedirs(TARGET_DIR, exist_ok=True)

# Remove old files
try: os.remove(os.path.join(TARGET_DIR, 'truth-evaders.apk'))
except: pass
try: os.remove(os.path.join(TARGET_DIR, 'truth-evaders.zip'))
except: pass

os.chdir('/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders')

with zipfile.ZipFile(os.path.join(TARGET_DIR, 'truth-evaders.apk'), 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('main.py', 'main.py')
    for root, dirs, files in os.walk('assets'):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path)
            
    # Include synthesis script so imported sounds work
    zipf.write('synth_retro_sounds.py', 'synth_retro_sounds.py')

shutil.copytree(TARGET_DIR, '/Users/rudil24/Documents/webdev/buzz-arcade/public/games/truth-evaders/', dirs_exist_ok=True)
print("Apk built and copied.")
