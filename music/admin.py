from django.contrib import admin

# Register your models here.
from .models import Artist, Song, List, Profile

admin.site.register([Artist, Song, List, Profile])