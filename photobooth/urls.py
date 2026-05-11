from django.urls import path
from . import views

app_name = 'photobooth'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('review/<uuid:session_id>/', views.review, name='review'),
    path('retake/<uuid:session_id>/<int:photo_index>/', views.retake_photo_ui, name='retake_photo_ui'),
    path('process-retake/<uuid:session_id>/<int:photo_index>/', views.process_retake, name='process_retake'),
    path('finalize/<uuid:session_id>/', views.finalize_session, name='finalize_session'),
    path('message/<uuid:session_id>/', views.message, name='message'),
    path('result/<uuid:session_id>/', views.result, name='result'),
]
