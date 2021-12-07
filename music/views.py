from django.shortcuts import render, HttpResponse
from .models import Artist, Song, List

# Create your views here.

def index(request):
    return HttpResponse("Hello! You are in the music root! :) Thank you Jesus!")

def all_artists(request):

    a_ = Artist.objects.all()

    data = ", ".join([artist.name for artist in a_])

    return HttpResponse(f"All artists => {data}")


def all_songs(request):

    a_ = Song.objects.all()

    data = ", ".join([song.title for song in a_])

    return HttpResponse(f"All songs => {data}")


def all_lists(request):

    a_ = List.objects.all()

    data = ", ".join([list.title for list in a_])

    return HttpResponse(f"All lists => {data}")