from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('Home', views.Base.as_view(), name='base'),
    path('', views.Home.as_view(), name='home'),

    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),

    # Genre URLs
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    path('genre/create/', views.GenreCreateView.as_view(), name='genre-create'),
    path('genre/<int:pk>/update/', views.GenreUpdateView.as_view(), name='genre-update'),
    path('genre/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre-delete'),

    # Book URLs
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    # Borrow URLs
    path('borrows/', views.BorrowListView.as_view(), name='borrow-list'),
    path('borrow/create/', views.BorrowCreateView.as_view(), name='borrow-create'),
    path('borrow/<int:pk>/update/', views.BorrowUpdateView.as_view(), name='borrow-update'),
    path('borrow/<int:pk>/delete/', views.BorrowDeleteView.as_view(), name='borrow-delete'),

    # Review URLs
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('review/create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),

    # Logout
    path('logout/', views.user_logout, name='logout'),
    path('login', views.login, name='login')
]

