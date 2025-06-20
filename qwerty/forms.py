from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Album, Artist, Genre
import datetime

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        default_html = super().render(name, value, attrs, **kwargs)
        if value and hasattr(value, 'url'):
            return f'''
                <div class="image-preview-container mb-3">
                    <img src="{value.url}" class="img-preview img-fluid mb-2" style="max-height: 200px;">
                    <div class="custom-file">
                        {default_html}
                    </div>
                </div>
            '''
        return default_html

class DateInput(forms.DateInput):
    input_type = 'date'

class AlbumForm(forms.ModelForm):
    def clean_release_date(self):
        date = self.cleaned_data['release_date']
        if date > datetime.date.today():
            raise ValidationError(_('Дата релиза не может быть в будущем'))
        return date

    class Meta:
        model = Album
        fields = ['title', 'release_date', 'price', 'label', 'genre', 'artists', 'cover_image']
        widgets = {
            'release_date': DateInput(),
            'cover_image': ImagePreviewWidget(),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }
        help_texts = {
            'cover_image': _('Рекомендуемый размер: 500x500 пикселей'),
            'price': _('Введите цену в рублях'),
            'release_date': _('Выберите дату релиза'),
        }

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'country', 'bio', 'image']
        widgets = {
            'image': ImagePreviewWidget(),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'image': _('Рекомендуемый размер: 400x400 пикселей'),
            'bio': _('Краткая биография исполнителя'),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description', 'image']
        widgets = {
            'image': ImagePreviewWidget(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'image': _('Рекомендуемый размер: 300x300 пикселей'),
            'description': _('Краткое описание жанра'),
        } 