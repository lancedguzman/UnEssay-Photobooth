from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence
import os
from django.conf import settings
import uuid

# Define the box coordinates (x, y) and target size for each design
# These are calculated based on the aspect ratios of your provided strips.
STRIP_CONFIG = {
    'photostrip.jpg': {
        'photo_size': (465, 340), # Landscape aspect ratio to match template
        'slots': [
            (65, 280),  # Top Photo
            (65, 645), # Middle Photo
            (65, 1015), # Bottom Photo
        ],
    }
}


def process_collage(image_files, template_name="photostrip.jpg"):
    """Stitches 3 photos onto the photostrip.jpg background."""
    template_path = os.path.join(settings.MEDIA_ROOT, 'photostrips', 'photostrip.jpg')
    
    try:
        canvas = Image.open(template_path).convert('RGB')
    except FileNotFoundError:
        # Fallback if file is missing
        canvas = Image.new('RGB', (834, 2480), (255, 255, 255))

    layout = STRIP_CONFIG['photostrip.jpg']
    target_width, target_height = layout['photo_size']
    slots = layout['slots']

    # Ensure we only use the 3 captured images
    images = [Image.open(f) for f in image_files[:3]]
    
    for i, img in enumerate(images):
        fitted_img = ImageOps.fit(img, (target_width, target_height), Image.Resampling.LANCZOS)
        canvas.paste(fitted_img, slots[i])

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


def add_message_to_image(relative_path, msg_iam, msg_reject):
    """Burns the 'I am' and 'I reject' messages into the appropriate spaces."""
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    if not os.path.exists(full_path): return

    with Image.open(full_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Adjust Y coordinates to sit below the printed "I AM" and "I REJECT" headers
        iam_y = int(height * 0.08)     # Space below "I AM"
        reject_y = int(height * 0.85)   # Space below "I REJECT"
        
        font_path = os.path.join(settings.BASE_DIR, 'media', 'fonts', 'Montserrat.ttf')
        try:
            font = ImageFont.truetype(font_path, size=75)
        except IOError:
            font = ImageFont.load_default()

        def draw_centered(text, target_y):
            if not text: return
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            draw.text(((width - text_w) / 2, target_y), text, font=font, fill=(0, 0, 0))

        draw_centered(msg_iam, iam_y)
        draw_centered(msg_reject, reject_y)
        img.save(full_path, quality=95)


def add_message_to_gif(relative_path, msg_iam, msg_reject):
    """Adds header and footer text to each frame of the GIF."""
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    
    if not os.path.exists(full_path):
        return

    with Image.open(full_path) as gif:
        frames = []
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'SpecialElite-Regular.ttf')
        try:
            font = ImageFont.truetype(font_path, size=24) # Slightly smaller font for GIFs
        except IOError:
            font = ImageFont.load_default()

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGB')
            width, height = frame.size
            
            # If the GIF frames don't natively include blank headers/footers, 
            # expand the canvas height dynamically to sandwich the animation:
            header_height = 60
            footer_height = 60
            new_height = height + header_height + footer_height
            
            # Create a base Canvas (Off-white/cream background)
            new_frame = Image.new('RGB', (width, new_height), (247, 244, 239))
            # Paste original frame in the middle
            new_frame.paste(frame, (0, header_height))
            
            draw = ImageDraw.Draw(new_frame)
            text_color = (93, 64, 55)

            # Helper for drawing on the extended canvas boundaries
            def draw_canvas_text(text, is_header=True):
                if not text:
                    return
                if hasattr(draw, 'textbbox'):
                    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                    text_w = right - left
                    text_h = bottom - top
                else:
                    text_w, text_h = draw.textsize(text, font=font)
                    
                text_x = (width - text_w) / 2
                if is_header:
                    text_y = (header_height - text_h) / 2
                else:
                    text_y = header_height + height + (footer_height - text_h) / 2
                    
                draw.text((text_x, text_y), text, font=font, fill=text_color)

            draw_canvas_text(msg_iam, is_header=True)
            draw_canvas_text(msg_reject, is_header=False)
            
            frames.append(new_frame)

        # Save frames back out as animated GIF
        frames[0].save(
            full_path,
            save_all=True,
            append_images=frames[1:],
            duration=gif.info.get('duration', 200),
            loop=0
        )