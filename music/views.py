from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics, permissions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from .models import Songs
from .serializers import SongsSerializer


class ListSongsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ListSongsView(generics.ListAPIView):
    """
    Provides a GET method handler
    """
    permission_classes = (permissions.AllowAny,)

    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('artist',)
    search_fields = ('title', 'artist')
    pagination_class = ListSongsPagination

class LoginView(generics.CreateAPIView):
    # This permission class will over ride the global permission
    # remove this in production, a valid token must be provided
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)


class SongCreate(generics.CreateAPIView):
    # remove this in production, a valid token must be provided
    permission_classes = (permissions.AllowAny,)

    serializer_class = SongsSerializer
    # override CreateAPIView create method
    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        artist = request.data.get('artist')
        if title is None:
            raise ValidationError({'title': 'You must provide a song title'})
        if artist is None:
            raise ValidationError({'artist': 'You must provide the song interpreter AKA artist'})
        return super().create(request, *args, **kwargs)


class SongDestroy(generics.DestroyAPIView):
    # remove this in production, a valid token must be provided
    permission_classes = (permissions.AllowAny,)

    queryset = Songs.objects.all()
    lookup_field = 'id'

    # override parent delete method in order to clean cache
    def delete(self, request, *args, **kwargs):
        song_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('songs_data_{}'.format(song_id))
        return response


class SongRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # remove this in production, a valid token must be provided
    permission_classes = (permissions.AllowAny,)

    queryset = Songs.objects.all()
    lookup_field = 'id'
    serializer_class = SongsSerializer

    # override parent delete & update methods in order to clean cache
    def delete(self, request, *args, **kwargs):
        song_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('songs_data_{}'.format(song_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            song = response.data
            cache.set('songs_data_{}'.format(song['id']), {
                'title': song['title'],
                'artist': song['artist']
            })
        return response