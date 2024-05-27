from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer, BookPatchSerializer
from rest_framework.views import Request, Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics


# Create your views here.
class BookModelViewSet(viewsets.ModelViewSet):
    def list(self, request: Request) -> Response:
        queryset = Book.objects.all()
        serialized = BookSerializer(queryset, many=True)
        return Response(serialized.data)

    def create(self, request: Request) -> Response:
        deserialized = BookSerializer(data=request.data)
        if not deserialized.is_valid():
            return Response(deserialized.errors, status=status.HTTP_400_BAD_REQUEST)
        deserialized.save()
        return Response(deserialized.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, book_id: int) -> Response:
        book = get_object_or_404(Book, pk=book_id)
        return Response(BookSerializer(book).data)

    def update(self, request: Request, book_id: int) -> Response:
        deserialized = BookSerializer(data=request.data)
        if not deserialized.is_valid():
            return Response(deserialized.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=book_id)
            book.title = deserialized.data['title']
            book.author = deserialized.data['author']
            book.genre = deserialized.data['genre']
            book.published_date = deserialized.data['published_date']
            book.price = deserialized.data['price']
            response_status = status.HTTP_200_OK
        except Book.DoesNotExist:
            book = Book.objects.create(**deserialized.validated_data)
            book.id = book_id
            response_status = status.HTTP_201_CREATED
        book.save()
        return Response(BookSerializer(book).data, status=response_status)

    def partial_update(self, request: Request, book_id: int) -> Response:
        book = get_object_or_404(Book, pk=book_id)
        # NOTE: BookSerializer won't work as it treats all the fields mandatory
        # In patch, we may not want to update all the fields at the same time.
        # Hence, a custom serializer is required: BookPatchSerializer(serializers.Serializer)
        deserialized = BookPatchSerializer(data=request.data) # BookSerializer(data=request.data)
        if not deserialized.is_valid():
            return Response(deserialized.errors, status=status.HTTP_400_BAD_REQUEST)
        deserialized.update(book, deserialized.validated_data)
        return Response(BookSerializer(book).data)

    def destroy(self, request: Request, book_id: int) -> Response:
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response({'message': 'Deleted book with id ' + str(book_id)})


# Filter based view
# Reference: https://www.django-rest-framework.org/api-guide/filtering/
class BookListAPIView(generics.ListAPIView):
    # queryset = Book.objects.all() # NOT REQUIRED
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author__iexact=author)
        genre = self.request.query_params.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre__iexact=genre)
        return queryset
    