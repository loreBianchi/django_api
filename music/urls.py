from django.urls import path
from .views import ListSongsView, LoginView, SongCreate, SongDestroy, SongRetrieveUpdateDestroy


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('songs/new', SongCreate.as_view(), name="songs-create"),
    path('songs/<int:id>/destroy', SongDestroy.as_view(), name='song-destroy'),
    path('songs/<int:id>/', SongRetrieveUpdateDestroy.as_view(), name='song'),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
]