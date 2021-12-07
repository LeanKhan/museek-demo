from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(default="default.jpg", upload_to="users/images")
    location = models.CharField(max_length=30, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Artist(models.Model):
    name = models.CharField(max_length=100)
    profile = models.URLField()
    genre = models.CharField(max_length=70)

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist,
                               on_delete=CASCADE,
                               related_name="songs",
                               related_query_name="song")
    duration = models.IntegerField(null=True, blank=True)
    mood = models.CharField(max_length=50)
    art = models.ImageField(upload_to="music/art")
    audio_file = models.FileField(null=True, blank=True, upload_to="music/songs")
    comment = models.TextField()
    link = models.URLField()
    likes = models.IntegerField(default=0)

    YOUTUBE = 'YT'
    SOUNDCLOUD = 'SC'
    AUDIO = 'AUD'

    SOURCES = [(YOUTUBE, 'YouTube'), (SOUNDCLOUD, 'Soundcloud'),
               (AUDIO, 'Audio File')]

    source = models.CharField(max_length=4, choices=SOURCES, default=YOUTUBE)

    def __str__(self) -> str:
        return f"'{self.title}' - {self.artist.name}"


class List(models.Model):
    title = models.CharField(max_length=200, default="Library")
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='library')
    description = models.TextField(default="My default music collection")
    songs = models.ManyToManyField(Song,  related_name="lists",
        related_query_name="list")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @receiver(post_save, sender=User)
    def create_user_library(sender, instance, created, **kwargs):
        if created:
            List.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_library(sender, instance, **kwargs):
        instance.library.save()

    def __str__(self) -> str:
        return f"@{self.user.username}'s {self.title}"

def delete_related_user(sender, instance, **kwargs):
    instance.user.delete()

post_delete.connect(delete_related_user, sender=Profile)