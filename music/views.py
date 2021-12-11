from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from .models import Artist, Song, List, Profile, User
from .forms import SignupForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "music/index.html", {"title": "Home"})

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

def user_home(request, username):

    user = get_object_or_404(User, username=username)

    ctx = {'library': user.library, 'u': user, 'songs': user.library.songs.all()}

    return render(request, 'music/user_home.html', ctx)

@login_required
def home(request):
    return redirect('music:user_home', username=request.user.username)