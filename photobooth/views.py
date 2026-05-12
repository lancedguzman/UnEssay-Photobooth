from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import os
from .models import PhotoSession, IndividualPhoto
from media_processing.services import add_message_to_image, add_message_to_gif, process_collage
from qr_generation.services import generate_qr_base64

def landing(request):
    return render(request, 'landing.html')


def review(request, session_id):
    session = get_object_or_404(PhotoSession, id=session_id)

    # Logic to restart entire session (mostly for GIF)
    if request.method == 'POST' and request.POST.get('action') == 'retake_session':
        if session.final_file and os.path.isfile(session.final_file.path):
            os.remove(session.final_file.path)
        session.delete()
        return redirect('photo_ui') 

    context = {'session': session}
    
    # Pass the 3 individual photos to the template
    if session.session_type == 'collage':
        context['photos'] = session.photos.all()

    return render(request, 'review.html', context)


def retake_photo_ui(request, session_id, photo_index):
    """Renders the single-photo camera."""
    session = get_object_or_404(PhotoSession, id=session_id)
    return render(request, 'single_retake.html', {
        'session_id': session.id,
        'photo_index': photo_index
    })


def process_retake(request, session_id, photo_index):
    """Updates one specific photo in the sequence."""
    if request.method == 'POST':
        session = get_object_or_404(PhotoSession, id=session_id)
        file = request.FILES.get('webcam_image')
        
        if file:
            # Find the specific slot (0, 1, or 2)
            photo = get_object_or_404(IndividualPhoto, session=session, index=photo_index)
            
            # Delete old file, save new one
            if photo.image:
                photo.image.delete(save=False)
            photo.image = file
            photo.save()
            
            return JsonResponse({'status': 'success', 'session_id': session.id})
            
    return JsonResponse({'status': 'error'})


def finalize_session(request, session_id):
    """
    Called when user clicks 'Looks Good'.
    Stitches the photos using the template saved in the session.
    """
    if request.method == 'POST':
        session = get_object_or_404(PhotoSession, id=session_id)
        photos = session.photos.all()
        
        # 🚨 REMOVE the hardcoded `photos.count() < 3` check
        if not photos.exists():
            return redirect('photobooth:review', session_id=session.id)

        image_files = [p.image for p in photos]
        template_choice = getattr(session, 'chosen_template', 'photostrip_1.jpg')
        
        final_path = process_collage(image_files, template_choice) 
        
        session.final_file = final_path
        session.save()
        
        return redirect('photobooth:message', session_id=session.id)
    
    return redirect('photobooth:review', session_id=session.id)


def message(request, session_id):
    """
    Renders the message input form and processes the submitted messages.
     - For GIFs: Passes both messages to the GIF burner.
     - For Images: Passes both messages to the standard Image burner.
    """
    session = get_object_or_404(PhotoSession, id=session_id)
    
    if request.method == 'POST':
        # Ensure these match the 'name' attributes in message.html exactly
        msg_iam = request.POST.get('message_iam', '').strip()
        msg_reject = request.POST.get('message_reject', '').strip()
        
        if session.final_file:
            # Pass them to the burner service
            add_message_to_image(session.final_file.name, msg_iam, msg_reject)
        
        return redirect('photobooth:result', session_id=session.id)
    
    return render(request, 'message.html', {'session': session})


def result(request, session_id):
    session = get_object_or_404(PhotoSession, id=session_id)
    
    # --- SAFETY CHECK ---
    # If there is no final file yet, redirect them back to the review page 
    # (or home) so they don't hit the ValueError.
    if not session.final_file:
        # Assuming 'review' is the URL name for the review view
        # Adjust 'landing' or 'review' based on your actual urls.py names
        return redirect('home') 
    # --------------------

    # Construct the Share URL dynamically
    host = request.get_host()
    scheme = request.scheme
    share_url = f"{scheme}://{host}{session.final_file.url}"
    direct_image_url = f"{scheme}://{host}{session.final_file.url}"
    
    # Call QR Service
    qr_code = generate_qr_base64(direct_image_url)
    
    context = {
        'session': session,
        'qr_code': qr_code,
        'share_url': share_url
    }
    return render(request, 'result.html', context)
