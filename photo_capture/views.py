from django.shortcuts import render
from django.http import JsonResponse
from photobooth.models import PhotoSession, IndividualPhoto

def capture_ui(request):
    """Renders the HTML specific to the photo session"""
    # 1. Grab the selected template from the URL (default to strip 1)
    selected_template = request.GET.get('template', 'photostrip_1.jpg') 
    
    return render(request, 'photo_ui.html', {'selected_template': selected_template})


def process_request(request):
    """
    Saves the captured photos individually.
    Dynamically expects 4 photos for strip 1, and 3 for the rest.
    """
    if request.method == 'POST':
        files = request.FILES.getlist('webcam_images[]')
        
        template_choice = request.POST.get('template_choice', 'photostrip_1.jpg')
        
        # DYNAMIC VALIDATION: Expect 4 photos for design 1 and 2
        expected_photos = 4 if template_choice in ['photostrip_1.jpg', 'photostrip_2.jpg', 'photostrip_3.jpg'] else 3
        
        if len(files) != expected_photos:
             return JsonResponse({'status': 'error', 'message': f'Need exactly {expected_photos} photos.'})

        session = PhotoSession.objects.create(
            session_type='collage',
            chosen_template=template_choice  
        )
        
        for i, file_data in enumerate(files):
            IndividualPhoto.objects.create(
                session=session,
                image=file_data,
                index=i
            )
        
        return JsonResponse({'status': 'success', 'session_id': session.id})

    return JsonResponse({'status': 'error'})
