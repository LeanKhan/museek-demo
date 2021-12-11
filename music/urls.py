from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from museek.settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_URL
from django.contrib.auth import views as auth_views

from . import views

app_name = 'music'
urlpatterns = [
    path('artists/', views.all_artists, name = 'All Artists'),
    path('songs/', views.all_songs, name = 'All Songs'),
    path('lists/', views.all_lists, name = 'All Lists'),
    path('home/', views.home, name="home"),
    path('@<str:username>/', views.user_home, name='user_home'),
    path('', views.index, name='index')
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)