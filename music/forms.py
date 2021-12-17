from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, \
ImageField, FileField, ModelChoiceField
from .models import List, Song, Artist
from django.utils.safestring import mark_safe


class SongForm(ModelForm):
    class Meta:
        model = Song
        exclude = ['likes', 'slug', 'uploaded_by']

    art = ImageField(required=False)

    artist = ModelChoiceField(queryset=Artist.objects.all(),
                                    help_text=mark_safe("Can't find an artist?<br />\
                                     <a class='btn btn-light btn-outline-info btn-sm' href='/artists/add?next=/songs/add'>Add them to Museek</a>"),
                                    required=False)


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        exclude = ['slug']


class AddSongToLibraryForm(ModelForm):
    class Meta:
        model = List
        fields = ['songs']

    songs = ModelMultipleChoiceField(queryset=Song.objects.all(),
                                     widget=CheckboxSelectMultiple,
                                     required=False)
