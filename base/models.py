from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Anime(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('tv', 'TV Show'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.ImageField(upload_to='anime_pic/')  
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    genres = models.ManyToManyField(Genre)
    total_episodes = models.CharField(max_length=2000,null=True, blank=True)
    uploaded_episodes = models.CharField(max_length=2000,null=True, blank=True)
    interval = models.CharField(max_length=12,null=True, blank=True)

    def __str__(self):
        return f"{self.title} - Total Episodes: {self.total_episodes}"


# signal to delete picture of particular anime
@receiver(post_delete, sender=Anime)
def delete_picture(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="episodes")
    name = models.CharField(max_length=200)
    episode_no = models.CharField(max_length=2000,null=True, blank=True) 
    video_url = models.URLField(max_length=4000)
 
    def __str__(self):
        return f"{self.anime.title} - {self.name}"




class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile_pic/')

    def __str__(self):
        return f"- {self.name}"


# signal to delete picture of user
@receiver(post_delete, sender=UserProfile)
def delete_picture(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path) 


class AnimeList(models.Model):
    CATEGORY_CHOICES = [
        ('watched', 'Watched'),
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, null=True, blank=True, related_name="animelist")  
    status =  models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.anime.title} - {self.status}"
