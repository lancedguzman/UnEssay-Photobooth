from django.shortcuts import render
from django.http import JsonResponse
from media_processing.services import process_gif, add_message_to_gif
from photobooth.models import PhotoSession

def capture_ui(request):
    # Renders HTML specific to GIF (maybe faster countdowns)
    return render(request, 'gif_ui.html')


def process_request(request):
    if request.method == 'POST':
        files = request.FILES.getlist('webcam_images[]')
        
        # 1. Get the message from the frontend
        user_msg = request.POST.get('user_message', '')
        
        file_path = process_gif(files)
        
        # 2. Save session with the message included
        session = PhotoSession.objects.create(
            session_type='gif',
            user_message=user_msg, 
            final_file=file_path
        )
        
        # 3. Burn the text onto the GIF
        if user_msg:
            # This edits the file on disk to include the text
            add_message_to_gif(session.final_file.name, user_msg)
        
        return JsonResponse({'status': 'success', 'session_id': session.id})
    return JsonResponse({'status': 'error'})
