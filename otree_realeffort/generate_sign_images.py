import string
import os
from PIL import Image, ImageDraw, ImageFont

def generate_letter_images(output_dir="letters"):
    os.makedirs(output_dir, exist_ok=True)
    chars = string.ascii_lowercase + string.digits

    # Try a larger Truetype font, fallback to default if not found
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except OSError:
        font = ImageFont.load_default()

    # We'll generate 100x100 images so you can see the characters more easily
    for ch in chars:
        img = Image.new('RGB', (100, 100), color='white')
        draw = ImageDraw.Draw(img)

        # The mask from font.getmask() returns the rendered glyph; we can measure it this way
        mask = font.getmask(ch)
        text_width, text_height = mask.size

        # Center the text in the 100x100 image
        x = (100 - text_width) // 2
        y = (100 - text_height) // 2

        draw.text((x, y), ch, fill='black', font=font)
        img.save(os.path.join(output_dir, f"{ch}.png"))

if __name__ == "__main__":
    generate_letter_images()
    print("Done! Letter images generated in the 'letters' folder.")