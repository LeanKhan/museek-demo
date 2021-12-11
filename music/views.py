from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from .models import Artist, Song, List, Profile, User
from .forms import SongForm, ArtistForm, AddSongToLibraryForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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

    add_song_form = AddSongToLibraryForm(instance=user.library)

    ctx = {'library': user.library, 'u': user, 'songs': user.library.songs.all(), 'add_song_form': add_song_form}

    return render(request, 'music/user_home.html', ctx)

@login_required
def add_song_to_library(request, username):
    if request.method == 'POST':
        add_song_form = AddSongToLibraryForm(request.POST, instance=request.user.library)
        if add_song_form.is_valid():
            add_song_form.save()
        else:
            print(list(add_song_form.errors))
            return redirect(reverse('music:user_home', kwargs={'username': request.user.username}) + "#add-song-to-library")


    return redirect('music:user_home', username=request.user.username)

@login_required
def home(request):
    return redirect('music:user_home', username=request.user.username)

@login_required
def add_song(request):
    form = SongForm()
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:all_songs')
            return redirect(next_url)
        # else:
        #     return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'music/song_form.html', {'form':form})

@login_required
def add_artist(request):
    form = ArtistForm()
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:all_artists')
            return redirect(next_url)
        # else:
        #     return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'music/artist_form.html', {'form':form})