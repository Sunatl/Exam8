from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ManyToManyField(Genre, related_name="books")
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to="book_covers/", null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"



