import zipfile
import os
import shutil

# Remove old files
try: os.remove('build/web/iceout.apk')
except: pass
try: os.remove('build/web/iceout.zip')
except: pass

with zipfile.ZipFile('build/web/iceout.apk', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('main.py', 'main.py')
    for root, dirs, files in os.walk('assets'):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path)

shutil.copytree('build/web', '/Users/rudil24/Documents/webdev/buzz-arcade/public/games/iceout/', dirs_exist_ok=True)
print("Apk built and copied.")
