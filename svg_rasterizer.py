import io
import cairosvg
from PIL import Image

def rasterize_svg_to_png(svg_bytes, width=128, height=128):
    if not svg_bytes:
        img = Image.new('RGB', (width, height), color=(0, 100, 0))
        return img
    png_data = cairosvg.svg2png(bytestring=svg_bytes, output_width=width, output_height=height)
    return Image.open(io.BytesIO(png_data)).convert('RGB')
    