from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank = True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=150)
    image = models.ImageField(blank=True, default='images/users/user.jpg',
                              upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):

        return f"{self.user.first_name} {self.user.last_name}"


    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')