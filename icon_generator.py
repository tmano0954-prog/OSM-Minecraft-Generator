from PIL import Image
import os

def create_world_icon(output_world_folder):
    img = Image.new('RGB', (64, 64), color=(34, 139, 34))
    img.save(os.path.join(output_world_folder, "icon.png"))
    