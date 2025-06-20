from rest_framework import serializers
from .models import Album, Artist, Genre, Label, Customer, Order, OrderItem

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'image']

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'image']

class AlbumSerializer(serializers.ModelSerializer):
    artists = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(),
        many=True
    )
    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all()
    )
    label = serializers.PrimaryKeyRelatedField(
        queryset=Label.objects.all()
    )

    class Meta:
        model = Album
        fields = [
            'id', 'title', 'artists', 'genre', 'label',
            'release_date', 'price', 'cover_image'
        ]

    def create(self, validated_data):
        artists = validated_data.pop('artists', [])
        album = Album.objects.create(**validated_data)
        album.artists.set(artists)
        return album

    def update(self, instance, validated_data):
        artists = validated_data.pop('artists', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if artists is not None:
            instance.artists.set(artists)
        return instance

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']

class OrderItemSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        source='album',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'album', 'album_id', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'total_amount', 'order_date', 'status']
        read_only_fields = ['total_amount'] 