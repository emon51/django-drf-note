
"""
===========================
MODELS (Database Layer)
===========================
"""

from django.db import models

# Parent Model
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Child Model (ForeignKey relationship)
class Book(models.Model):
    title = models.CharField(max_length=100)

    # Relationship: One Author → Many Books
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"   # reverse access: author.books.all()
    )

    def __str__(self):
        return self.title


"""
===========================
SERIALIZERS (Data Layer)
===========================
"""

from rest_framework import serializers

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


# Author Serializer (Nested Serializer Example)
class AuthorSerializer(serializers.ModelSerializer):

    # Nested relationship (Author → Books)
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]


"""
===========================
VIEWS (API Layer)
===========================
"""

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


# Pagination class
class StandardPagination(PageNumberPagination):
    page_size = 5


# List + Create API (Author)
class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    permission_classes = [IsAuthenticated]   # authentication required
    pagination_class = StandardPagination    # pagination enabled

    # filtering example
    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            return Author.objects.filter(name__icontains=name)
        return Author.objects.all()

    # custom create logic
    def perform_create(self, serializer):
        serializer.save()


# Retrieve + Update + Delete API (Author Detail)
class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "pk"  # default, can be email/slug etc.


"""
===========================
URLS (Routing Layer)
===========================
"""

from django.urls import path

urlpatterns = [
    # List + Create
    path("authors/", AuthorListCreateView.as_view()),

    # Retrieve + Update + Delete
    path("authors/<int:pk>/", AuthorDetailView.as_view()),
]


"""
===========================
API BEHAVIOR SUMMARY
===========================

GET    /authors/        # list authors (with books nested)
POST   /authors/        # create author
GET    /authors/1/      # single author
PUT    /authors/1/      # update
DELETE /authors/1/      # delete

===========================
"""
