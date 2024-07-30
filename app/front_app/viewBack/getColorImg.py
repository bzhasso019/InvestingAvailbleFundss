from PIL import Image
from colorthief import ColorThief
import io

def getColorImg(image_paths):
    if len(image_paths) == 0:
        return []
    dominant_colors = []
    for image_path in image_paths:
        image = Image.open(f'app/static/logo_org/{image_path}')
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        dominant_colors.append(ColorThief(image_bytes).get_color(quality=1))

    images_with_colors = []
    for image_path, color in zip(image_paths, dominant_colors):
        images_with_colors.append(f'rgb{color}')

    return images_with_colors