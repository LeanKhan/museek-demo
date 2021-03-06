from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from .models import Artist, Song, List, Profile, User
from .forms import SongForm, ArtistForm, AddSongToLibraryForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import UpdateView

# Create your views here.

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['fullname', 'bio', 'location']

    template_name = "music/profile_form.html"

    def get_success_url(self) -> str:
        return reverse("music:user_home", kwargs={"username": self.get_object().user.username})

def index(request):
    return render(request, "music/index.html", {"title": "Home"})

def all_artists(request):

    artists = Artist.objects.all()

    ctx = {'artists': artists}

    return render(request, 'music/all_artists.html', ctx)


def all_songs(request):

    songs = Song.objects.all()

    ctx = {'songs': songs}

    return render(request, 'music/all_songs.html', ctx)


def all_libraries(request):

    libs = List.objects.all()

    ctx = {'libraries': libs}

    return render(request, 'music/all_libraries.html', ctx)


def all_lists(request):

    a_ = List.objects.all()

    data = ", ".join([list.title for list in a_])

    return HttpResponse(f"All lists => {data}")

def user_home(request, username):

    user = get_object_or_404(User, username=username)

    add_song_form = AddSongToLibraryForm(instance=user.library)

    suggested_libraries = List.objects.exclude(user=request.user)

    ctx = {'library': user.library, 'u': user, 'songs': user.library.songs.all(),
     'add_song_form': add_song_form, 'suggested_libraries': suggested_libraries}

    return render(request, 'music/user_home.html', ctx)

def view_artist(request, slug, id):

    artist = get_object_or_404(Artist, id=id)

    ctx = {'artist': artist}

    return render(request, 'music/view_artist.html', ctx)

def view_song(request, slug, id):

    song = get_object_or_404(Song, id=id)

    ctx = {'song': song}

    return render(request, 'music/view_song.html', ctx)

@login_required
def update_song(request, slug, id):

    song = get_object_or_404(Song, id=id)
    # if uploaded by someone else...
    if song.uploaded_by and song.uploaded_by != request.user:
        return HttpResponse("""<h1 class="display-4">Unauthorized mehn!</h1> <p><a href = "/">Back home</a></p>""")
    song_form = SongForm(request.POST or None, instance=song)
    if request.method == 'POST':
        if song_form.is_valid():
            song_form.save()
            next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:view_song',
             kwargs={"slug": song.slug, "id": song.id})
            return redirect(next_url)
        # else:
        #     return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'music/update_song_form.html', {'form':song_form, 'song': song})

# update song
@login_required
def delete_song(request, slug, id):
    song = get_object_or_404(Song, id=id)

    try:
        song.delete()
    except:
        return HttpResponse("""<h1 class="display-4">Error deleting Song!</h1> <p><a href = "/">Back home</a></p>""")

    next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:all_songs')
    return redirect(next_url)

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

# liking a song is the same as adding it to your library...
@login_required
def toggle_like_song(request, slug, id):
    if request.method == 'POST':

        # get user library, get song

        song = get_object_or_404(Song, id=id)

        if song in request.user.library.songs.all():
            request.user.library.songs.remove(song)
        else:
            request.user.library.songs.add(song)

        request.user.library.save()

    next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:user_home', kwargs={"username": request.user.username})
    return redirect(next_url)

@login_required
def home(request):
    return redirect('music:user_home', username=request.user.username)

@login_required
def add_song(request):
    form = SongForm()
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            sng = form.save(commit=False)

            sng.uploaded_by = request.user

            sng.save()

            if request.POST.get('add_to_library'):
                request.user.library.songs.add(sng)

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


# update artist
@login_required
def update_artist(request, slug, id):

    artist = get_object_or_404(Artist, id=id)
    # if uploaded by someone else...

    artist_form = ArtistForm(request.POST or None, instance=artist)
    if request.method == 'POST':
        if artist_form.is_valid():
            artist_form.save()
            next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:view_artist',
             kwargs={"slug": artist.slug, "id": artist.id})
            return redirect(next_url)
        # else:
        #     return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'music/update_artist_form.html', {'form':artist_form, 'artist': artist})

# delete artist
@login_required
def delete_artist(request, slug, id):
    artist = get_object_or_404(Artist, id=id)

    try:
        artist.delete()
    except:
        return HttpResponse("""<h1 class="display-4">Error deleting Artist!</h1> <p><a href = "/">Back home</a></p>""")

    next_url = request.POST.get('next') if request.POST.get('next') else reverse('music:all_artists')
    return redirect(next_url)