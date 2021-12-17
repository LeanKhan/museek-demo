from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from museek.settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_URL
from django.contrib.auth import views as auth_views

from . import views

app_name = 'music'
urlpatterns = [
    path('artists/', views.all_artists, name = 'all_artists'),
    path('artists/add', views.add_artist, name='add_artist'), # create
    path('artists/<slug:slug>/<int:id>', views.view_artist, name='view_artist'), # read
    path('artists/<slug:slug>/<int:id>/edit', views.update_artist, name='update_artist'), # update
    path('artists/<slug:slug>/<int:id>/delete', views.delete_artist, name='delete_artist'), # delete
    # song routes
    path('songs/', views.all_songs, name = 'all_songs'),
    path('songs/add', views.add_song, name='add_song'), # create
    path('songs/<slug:slug>/<int:id>', views.view_song, name='view_song'), # read
    path('songs/<slug:slug>/<int:id>/edit', views.update_song, name='update_song'), # update
    path('songs/<slug:slug>/<int:id>/delete', views.delete_song, name='delete_song'), # delete
    path('songs/<slug:slug>/<int:id>/toggle-like', views.toggle_like_song, name='toggle_like_song'), # delete
    # others
    path('lists/', views.all_lists, name = 'all_lists'), # can ignore
    path('libraries/', views.all_libraries, name = 'all_libraries'),
    path('home/', views.home, name="home"),
    path('@<str:username>/', views.user_home, name='user_home'),
    path('users/<int:pk>/update/', views.ProfileUpdate.as_view(), name='update_profile'),
    path('@<str:username>/add', views.add_song_to_library, name='add_song_to_library'),
    path('', views.index, name='index')
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)