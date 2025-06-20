from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='register'), name='logout'),
    path('home/', views.info, name='info'),
    
    path('albums/', views.AlbumListView.as_view(), name='album-list'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('albums/create/', views.album_create, name='album-create'),
    path('albums/<int:pk>/update/', views.album_update, name='album-update'),
    path('albums/<int:pk>/delete/', views.album_delete, name='album-delete'),
    
    path('artists/', views.ArtistListView.as_view(), name='artist-list'),
    path('artists/<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('artists/create/', views.artist_create, name='artist-create'),
    path('artists/<int:pk>/update/', views.artist_update, name='artist-update'),
    path('artists/<int:pk>/delete/', views.artist_delete, name='artist-delete'),
    
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    path('genres/create/', views.genre_create, name='genre-create'),
    path('genres/<int:pk>/update/', views.genre_update, name='genre-update'),
    path('genres/<int:pk>/delete/', views.genre_delete, name='genre-delete'),
]
