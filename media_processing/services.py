from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence
import os
from django.conf import settings
import uuid

# Define the box coordinates (x, y) and target size for each design
# These are calculated based on the aspect ratios of your provided strips.
STRIP_CONFIG = {
    # Design 1: Classic White (Header on top)
    'photostrip_1.jpg': {
        'photo_size': (490, 325),
        'slots': [(55, 345), (55, 695), (55, 1045), (55, 1395)],
    },
    # Design 2: Wisteria Purple (Footer on bottom, slightly larger frames)
    'photostrip_2.jpg': {
        'photo_size': (490, 320),
        'slots': [(60, 150), (60, 505), (60, 855), (60, 1205)],
    },
    # Design 3: Chalkboard Dark (Footer on bottom)
    'photostrip_3.jpg': {
        'photo_size': (520, 350),
        'slots': [(40, 60), (40, 425), (40, 790), (40, 1150)],
    }
}


def process_collage(image_files, template_name="photostrip_1.jpg"):
    """
    Stitches 3 photos onto the selected template background.
    """
    template_path = os.path.join(settings.MEDIA_ROOT, 'photostrips', template_name)
    
    try:
        canvas = Image.open(template_path).convert('RGB')
    except FileNotFoundError:
        canvas = Image.new('RGB', (800, 2400), (247, 244, 239))
        template_name = 'photostrip_1.jpg'

    layout = STRIP_CONFIG.get(template_name, STRIP_CONFIG['photostrip_1.jpg'])
    target_width, target_height = layout['photo_size']
    slots = layout['slots']

    # 🚨 DYNAMIC UPDATE: Use len(slots) instead of [:3]
    images = [Image.open(f) for f in image_files[:len(slots)]]
    
    for i, img in enumerate(images):
        fitted_img = ImageOps.fit(img, (target_width, target_height), Image.Resampling.LANCZOS)
        
        paste_coords = slots[i]
        canvas.paste(fitted_img, paste_coords)

    filename = f"collage_{uuid.uuid4().hex[:8]}.jpg"
    relative_path = os.path.join('captures', filename)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    canvas.save(full_path, quality=95)
    
    return relative_path


def process_gif(image_files, message=""):
    """
    Accepts list of files, creates GIF, returns relative path.
    """
    images = [Image.open(f).resize((320, 240)) for f in image_files] # Smaller for GIF
    
    filename = f"gif_{uuid.uuid4().hex[:8]}.gif"
    full_path = os.path.join(settings.MEDIA_ROOT, 'captures', filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    images[0].save(
        full_path,
        save_all=True,
        append_images=images[1:],
        duration=200,
        loop=0
    )
    return f"captures/{filename}"


def add_message_to_image(image_relative_path, message):
    """
    Opens the existing image, adds a vintage footer with the message,
    and overwrites the file.
    """
    if not message:
        return image_relative_path

    full_path = os.path.join(settings.MEDIA_ROOT, image_relative_path)
    
    # 1. POINT TO YOUR CUSTOM FONT HERE
    font_path = os.path.join(settings.MEDIA_ROOT, 'fonts', 'Sacramento-Regular.ttf')
    
    try:
        # Use a context manager to ensure file is closed before saving
        with Image.open(full_path) as img:
            width, height = img.size
            
            # Define footer size
            footer_height = 180
            new_height = height + footer_height
            
            # Create new canvas (Vintage Cream Color)
            new_img = Image.new('RGB', (width, new_height), (247, 244, 239))
            new_img.paste(img, (0, 0))
            
            draw = ImageDraw.Draw(new_img)
            
            # 2. LOAD THE CUSTOM FONT
            try:
                font = ImageFont.truetype(font_path, 70) # Size 70 looks good for Sacramento
            except OSError:
                print("Sacramento font not found! Using default.")
                font = ImageFont.load_default()

            # Calculate text size to center it
            if hasattr(draw, 'textbbox'):
                left, top, right, bottom = draw.textbbox((0, 0), message, font=font)
                text_w = right - left
                text_h = bottom - top
            else:
                text_w, text_h = draw.textsize(message, font=font)

            text_x = (width - text_w) / 2
            # Adjust vertical center slightly
            text_y = height + (footer_height - text_h) / 2 - 10
            
            # Draw text (Vintage Brown)
            draw.text((text_x, text_y), message, font=font, fill=(93, 64, 55))
            
            # Save (Overwrite)
            new_img.save(full_path, quality=95)
            
            return image_relative_path

    except Exception as e:
        print(f"Error adding text to image: {e}")
        return image_relative_path
    

def add_message_to_gif(image_relative_path, message):
    """
    Splits a GIF, adds the vintage footer/text to EVERY frame,
    and saves it back as an animated GIF.
    """
    if not message:
        return image_relative_path

    full_path = os.path.join(settings.MEDIA_ROOT, image_relative_path)
    font_path = os.path.join(settings.MEDIA_ROOT, 'fonts', 'Sacramento-Regular.ttf')

    try:
        # Load the font once
        try:
            font = ImageFont.truetype(font_path, 50) # Slightly smaller for GIF (320px wide)
        except OSError:
            font = ImageFont.load_default()

        frames = []
        with Image.open(full_path) as img:
            # Iterate over every frame in the animation
            for frame in ImageSequence.Iterator(img):
                frame = frame.convert('RGB')
                
                width, height = frame.size
                footer_height = 80 # Smaller footer for smaller GIF
                new_height = height + footer_height
                
                # Create Canvas
                new_frame = Image.new('RGB', (width, new_height), (247, 244, 239))
                new_frame.paste(frame, (0, 0))
                
                draw = ImageDraw.Draw(new_frame)
                
                # Center Text
                if hasattr(draw, 'textbbox'):
                    left, top, right, bottom = draw.textbbox((0, 0), message, font=font)
                    text_w = right - left
                    text_h = bottom - top
                else:
                    text_w, text_h = draw.textsize(message, font=font)
                
                text_x = (width - text_w) / 2
                text_y = height + (footer_height - text_h) / 2 - 5
                
                draw.text((text_x, text_y), message, font=font, fill=(93, 64, 55))
                
                frames.append(new_frame)

        # Save frames as new GIF
        frames[0].save(
            full_path,
            save_all=True,
            append_images=frames[1:],
            duration=200, # Keep original speed
            loop=0
        )
        return image_relative_path

    except Exception as e:
        print(f"Error burning text to GIF: {e}")
        return image_relative_path
