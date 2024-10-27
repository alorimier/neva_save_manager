import glob
import os
from PIL import Image

ROOT_DIR = "resources\\Saves"

images = glob.glob(root_dir=ROOT_DIR, pathname="*\\*.png", recursive=True)

for image in images:
    img = Image.open(os.path.join(ROOT_DIR, image))
    new_img = img.resize((384, 216))
    new_img.save(os.path.join(ROOT_DIR, image))