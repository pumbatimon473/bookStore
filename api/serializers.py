from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookPatchSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=False)
    author = serializers.CharField(max_length=50, required=False)
    genre = serializers.CharField(max_length=20, required=False)
    published_date = serializers.DateField(required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)

    def create(self, validated_data: dict) -> Book:
        return Book.objects.create(**validated_data)

    def update(self, instance: Book, validated_data: dict) -> Book:
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
