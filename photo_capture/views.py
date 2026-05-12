from django.shortcuts import render
from django.http import JsonResponse
from photobooth.models import PhotoSession, IndividualPhoto

# views.py modifications
def capture_ui(request):
    """Renders the HTML specific to the photo session"""
    # Force the template to your specific photostrip
    return render(request, 'photo_ui.html', {'selected_template': 'photostrip.jpg'})


def process_request(request):
    """Saves the 3 captured photos individually."""
    if request.method == 'POST':
        files = request.FILES.getlist('webcam_images[]')
        
        # Hardcode to 3 photos as per your requirement
        expected_photos = 3 
        
        if len(files) != expected_photos:
             return JsonResponse({'status': 'error', 'message': f'Need exactly {expected_photos} photos.'})

        session = PhotoSession.objects.create(
            session_type='collage',
            chosen_template='photostrip.jpg'  
        )
        
        for i, file_data in enumerate(files):
            IndividualPhoto.objects.create(
                session=session,
                image=file_data,
                index=i
            )
        
        return JsonResponse({'status': 'success', 'session_id': session.id})

    return JsonResponse({'status': 'error'})
