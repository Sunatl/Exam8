from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    
    # Функция барои баргардонидани номи пурраи корбар
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    # Функция барои ҳисоб кардани синни муаллиф
    def age(self):
        if self.birth_date:
            if self.death_date:
                return (self.death_date - self.birth_date).days // 365
            return (now().date() - self.birth_date).days // 365
        return None

    def is_alive(self):
        return self.death_date is None


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def book_count(self):
        return self.books.count()


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ManyToManyField(Genre, related_name="books")
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to="static/images", null=True,blank=True )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Функция барои баргардонидани миқдори жанрҳо
    def genre_list(self):
        return ", ".join([genre.name for genre in self.genre.all()])

    # Функция барои санҷидани, ки китоб дастрас аст ё не
    def is_borrowed(self):
        return not self.is_available


class Borrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    # Функция барои санҷидани мӯҳлати бозгашт
    def is_overdue(self):
        if self.return_date and  self.is_returned:
            return now() > self.return_date
        return False

    # Функция барои ҳисоб кардани мӯҳлати қарз
    def borrowing_period(self):
        if self.return_date:
            return (self.return_date - self.borrow_date).days
        return None


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"

    # Функция барои нишон додани ситораҳо ба таври графикӣ
    def stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)
