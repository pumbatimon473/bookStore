from django.contrib import admin
from .models import Book


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'published_date', 'price')
    list_filter = ('author', 'genre')
    search_fields = ('title', 'author')