from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from museek.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artists/', views.all_artists, name = 'All Artists'),
    path('songs/', views.all_songs, name = 'All Songs'),
    path('lists/', views.all_lists, name = 'All Lists')
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)