from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    # on_delete : User 객체가 지워질 때 Profile 객체가 취할 행동?
    # related_name : user 객체에서 현재 Profile 객체를 바로 불러올 수 있도록 함. user.profile과 같은 형식으로
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # media_root밑에 profile이라는 경로가 추가되어 들어감. collect하나보다 나중에
    image = models.ImageField(upload_to='profile/', null=True)
    nickname = models.CharField(max_length=20, unique=True, null=True)
    message = models.CharField(max_length=100, null=True)