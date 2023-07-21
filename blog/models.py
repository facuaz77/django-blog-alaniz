from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# ------------


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def following(self):
        user_ids = Relations.objects.filter(from_user=self.user)\
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)
    
    def followers(self):
        user_ids = Relations.objects.filter(to_user=self.user)\
            .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    audio = models.FileField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)

    def delete_post(self):
        self.delete()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.content}'
    


class Relations(models.Model):
    from_user = models.ForeignKey(User, related_name='relations', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"
    
    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user',])
        ]

# ------------------------------
