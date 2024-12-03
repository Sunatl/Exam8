from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import Author, Genre, Book, Borrow, Review
from .forms import AuthorForm, GenreForm, BookForm, BorrowForm, ReviewForm

# Логикаи логин
@login_required
def user_logout(request):
    logout(request) 
    return render(request, 'registration/log_out.html') 

def login(request):
    return redirect("accounts/login/")

# Интихоби шаблон барои "Home" ё саҳифаи асосӣ
class Base(TemplateView):
    template_name = "base.html"
class Home(TemplateView):
    template_name = "home.html"

# Base ListView with Search functionality
class BaseListView(ListView):
    search_param = "search"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get(self.search_param, "")
        if search_query:
            queryset = self.apply_search(queryset, search_query)
        return queryset

    def apply_search(self, queryset, search_query):
        # Дар BaseListView функсияи ҷустуҷӯ танҳо хати умумиро амалӣ мекунад.
        return queryset  # Бо ҳама амалҳо барои ҷустуҷӯ дар Views-ҳои махсус тартиб дода мешавад

# Author Views
class AuthorListView(BaseListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'

    def apply_search(self, queryset, search_query):
        return queryset.filter(Q(name__icontains=search_query) | Q(biography__icontains=search_query))

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = reverse_lazy('author-list')

class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = reverse_lazy('author-list')
    


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = reverse_lazy('author-list')
    


# Genre Views
class GenreListView(BaseListView):
    model = Genre
    template_name = 'genre_list.html'
    context_object_name = 'genres'

    def apply_search(self, queryset, search_query):
        return queryset.filter(name__icontains=search_query)

class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genre_detail.html'
    context_object_name = 'genre'

class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'genre_form.html'
    success_url = reverse_lazy('genre-list')

class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'genre_form.html'
    success_url = reverse_lazy('genre-list')

class GenreDeleteView(DeleteView):
    model = Genre
    template_name = 'genre_confirm_delete.html'
    success_url = reverse_lazy('genre-list')

# Book Views
class BookListView(BaseListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def apply_search(self, queryset, search_query):
        return queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(author__name__icontains=search_query)
        )

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book-list')

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book-list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

# Borrow Views
class BorrowListView(BaseListView):
    model = Borrow
    template_name = 'borrow_list.html'
    context_object_name = 'borrows'

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user)

    def apply_search(self, queryset, search_query):
        return queryset.filter(
            Q(book__title__icontains=search_query)
        )

class BorrowCreateView(CreateView):
    model = Borrow
    form_class = BorrowForm
    template_name = 'borrow_form.html'
    success_url = reverse_lazy('borrow-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BorrowUpdateView(UpdateView):
    model = Borrow
    form_class = BorrowForm
    template_name = 'borrow_form.html'
    success_url = reverse_lazy('borrow-list')

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user)

class BorrowDeleteView(DeleteView):
    model = Borrow
    template_name = 'borrow_confirm_delete.html'
    success_url = reverse_lazy('borrow-list')

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user)

# Review Views
class ReviewListView(BaseListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(user = self.request.user)

    def apply_search(self, queryset, search_query):
        return queryset.filter(
            Q(book__title__icontains=search_query) |
            Q(review_text__icontains=search_query)
        )

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review-list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review-list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)