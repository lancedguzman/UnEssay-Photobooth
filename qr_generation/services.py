import qrcode
import io
import base64

def generate_qr_base64(url_data):
    """
    Generates a QR code for the given URL and returns a base64 string
    ready for HTML display (e.g., "data:image/png;base64,...").
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"
