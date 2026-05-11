import uuid
from django.db import models

class PhotoSession(models.Model):
    TYPE_CHOICES = [
        # Updated label since it can now be 3 or 4 photos
        ('collage', 'Photostrip Collage'), 
        ('gif', 'Animated GIF'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    session_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    chosen_template = models.CharField(max_length=50, default='photostrip_1.jpg')
    user_message = models.CharField(max_length=200, blank=True)
    final_file = models.FileField(upload_to='captures/')

    def __str__(self):
        return f"{self.session_type} - {self.id}"


class IndividualPhoto(models.Model):
    # related_name='photos' is CRITICAL. It allows session.photos.all() to work[cite: 13].
    session = models.ForeignKey(PhotoSession, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='individual_photos/')
    # Updated comment: Now tracks order dynamically (0, 1, 2, 3...)
    index = models.PositiveIntegerField() 

    class Meta:
        ordering = ['index']
        unique_together = ('session', 'index')