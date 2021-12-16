from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from museek.settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_URL
from django.contrib.auth import views as auth_views

from . import views

app_name = 'music'
urlpatterns = [
    path('artists/', views.all_artists, name = 'all_artists'),
    path('artists/add', views.add_artist, name='add_artist'),
    path('artists/<slug:slug>/<int:id>', views.view_artist, name='view_artist'),
    path('songs/', views.all_songs, name = 'all_songs'),
    path('songs/add', views.add_song, name='add_song'),
    path('songs/<slug:slug>/<int:id>', views.view_song, name='view_song'),
    path('lists/', views.all_lists, name = 'all_lists'),
    path('libraries/', views.all_libraries, name = 'all_libraries'),
    path('home/', views.home, name="home"),
    path('@<str:username>/', views.user_home, name='user_home'),
    path('@<str:username>/add', views.add_song_to_library, name='add_song_to_library'),
    path('', views.index, name='index')
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)