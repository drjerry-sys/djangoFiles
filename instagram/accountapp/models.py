from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your models here.
class UserProfile(models.Model):
    CHOICES = (('M', 'Male'), ('F', 'Female'), ('S', 'Shemale'), ('', 'Prefer not to Say'))
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=11, null=True, default='M', choices=CHOICES)
    bio = models.TextField(null=True, blank=True)
    profile_pics = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)

    # def get_absolute_url(self): pass

class SaveSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    device_family = models.CharField(null=False, max_length=500)
    device_browser = models.CharField(null=False, max_length=50)
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(auto_now=True)