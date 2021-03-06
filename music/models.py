from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_lifecycle import LifecycleModelMixin, AFTER_CREATE, AFTER_UPDATE, BEFORE_CREATE, BEFORE_UPDATE, hook

# Create your models here.

class Profile(LifecycleModelMixin, models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)

    fullname = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Artist(LifecycleModelMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    profile = models.URLField()
    genre = models.CharField(max_length=70)

    def get_absolute_url(self):
        return reverse('music:view_artist', kwargs={'slug': self.slug, 'id': self.id})

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when='name', has_changed=True, is_not=None)
    def update_slug(self):
        # works now! Thank you Jesus!
        self.slug = slugify(self.name)

    def __str__(self) -> str:
        return self.name


class Song(LifecycleModelMixin, models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist,
                               on_delete=CASCADE,
                               related_name="songs",
                               related_query_name="song")
    slug = models.SlugField(null=True)
    duration = models.IntegerField(null=True, blank=True)
    mood = models.CharField(max_length=50)
    comment = models.TextField()
    link = models.URLField()
    uploaded_by = models.ForeignKey(User, null=True, on_delete=SET_NULL)

    YOUTUBE = 'YT'
    SOUNDCLOUD = 'SC'
    SPOTIFY = 'SP'

    SOURCES = [(YOUTUBE, 'YouTube'), (SOUNDCLOUD, 'Soundcloud'),
               (SPOTIFY, 'Spotify')]

    source = models.CharField(max_length=4, choices=SOURCES, default=YOUTUBE)

    def get_absolute_url(self):
        return reverse('music:view_song', kwargs={'slug': self.slug, 'id': self.id})

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when='title', has_changed=True, is_not=None)
    def update_slug(self):
        self.slug = slugify(self.title)

    def __str__(self) -> str:
        return f"'{self.title}' - {self.artist.name}"


class List(LifecycleModelMixin, models.Model):
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

    def get_absolute_url(self):
        return reverse('music:user_home', kwargs={'username': self.user.username})

    def __str__(self) -> str:
        return f"@{self.user.username}'s {self.title}"

def delete_related_user(sender, instance, **kwargs):
    instance.user.delete()

post_delete.connect(delete_related_user, sender=Profile)