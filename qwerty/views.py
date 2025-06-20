from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Album, Artist, Genre, Track, Label, AlbumArtist
from .decorators import admin_required
from .forms import AlbumForm, ArtistForm, GenreForm

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'qwerty/register.html'
    success_url = reverse_lazy('info')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('info')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.save())
        messages.success(self.request, 'Регистрация успешно завершена!')
        return response

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'qwerty/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('info')

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)

@login_required
def info(request):
    albums = Album.objects.all().order_by('-id')[:6]  # Получаем 6 последних альбомов
    return render(request, 'qwerty/info.html', {'albums': albums})

# Альбомы
class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'qwerty/album_list.html'
    context_object_name = 'albums'
    ordering = ['-release_date']
    paginate_by = 9  # Количество альбомов на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        genre = self.request.GET.get('genre')
        artist = self.request.GET.get('artist')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(artists__name__icontains=search_query) |
                Q(genre__name__icontains=search_query)
            ).distinct()
        
        if genre:
            queryset = queryset.filter(genre__name=genre)
        if artist:
            queryset = queryset.filter(artists__name=artist)

        return queryset.select_related('genre', 'label').prefetch_related('artists')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['artists'] = Artist.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        return context

class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'qwerty/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = self.object.track_set.all()
        return context

@admin_required
def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save()
            messages.success(request, 'Альбом успешно создан!')
            return redirect('album-detail', pk=album.pk)
    else:
        form = AlbumForm()
    return render(request, 'qwerty/album_form.html', {'form': form, 'title': 'Создать альбом'})

@admin_required
def album_update(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            album = form.save()
            messages.success(request, 'Альбом успешно обновлен!')
            return redirect('album-detail', pk=album.pk)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'qwerty/album_form.html', {'form': form, 'title': 'Редактировать альбом'})

@admin_required
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Альбом успешно удален!')
        return redirect('album-list')
    return render(request, 'qwerty/album_confirm_delete.html', {'album': album})

# Исполнители
class ArtistListView(LoginRequiredMixin, ListView):
    model = Artist
    template_name = 'qwerty/artist_list.html'
    context_object_name = 'artists'
    ordering = ['name']
    paginate_by = 12  # Количество исполнителей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class ArtistDetailView(LoginRequiredMixin, DetailView):
    model = Artist
    template_name = 'qwerty/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = self.object.album_set.all()
        return context

@admin_required
def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            artist = form.save()
            messages.success(request, 'Исполнитель успешно создан!')
            return redirect('artist-detail', pk=artist.pk)
    else:
        form = ArtistForm()
    return render(request, 'qwerty/artist_form.html', {'form': form, 'title': 'Создать исполнителя'})

@admin_required
def artist_update(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            artist = form.save()
            messages.success(request, 'Исполнитель успешно обновлен!')
            return redirect('artist-detail', pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'qwerty/artist_form.html', {'form': form, 'title': 'Редактировать исполнителя'})

@admin_required
def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        artist.delete()
        messages.success(request, 'Исполнитель успешно удален!')
        return redirect('artist-list')
    return render(request, 'qwerty/artist_confirm_delete.html', {'artist': artist})

# Жанры
class GenreListView(LoginRequiredMixin, ListView):
    model = Genre
    template_name = 'qwerty/genre_list.html'
    context_object_name = 'genres'
    ordering = ['name']
    paginate_by = 12  # Количество жанров на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class GenreDetailView(LoginRequiredMixin, DetailView):
    model = Genre
    template_name = 'qwerty/genre_detail.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = self.object.album_set.all()
        return context

@admin_required
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES)
        if form.is_valid():
            genre = form.save()
            messages.success(request, 'Жанр успешно создан!')
            return redirect('genre-detail', pk=genre.pk)
    else:
        form = GenreForm()
    return render(request, 'qwerty/genre_form.html', {'form': form, 'title': 'Создать жанр'})

@admin_required
def genre_update(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES, instance=genre)
        if form.is_valid():
            genre = form.save()
            messages.success(request, 'Жанр успешно обновлен!')
            return redirect('genre-detail', pk=genre.pk)
    else:
        form = GenreForm(instance=genre)
    return render(request, 'qwerty/genre_form.html', {'form': form, 'title': 'Редактировать жанр'})

@admin_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Жанр успешно удален!')
        return redirect('genre-list')
    return render(request, 'qwerty/genre_confirm_delete.html', {'genre': genre})