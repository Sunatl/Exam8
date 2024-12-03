from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'phone_number','email', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
    
    

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography', 'birth_date', 'death_date']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'genre', 'publication_date', 'cover_image', 'is_available']

    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = [ 'book', 'return_date', 'is_returned']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [ 'book', 'review_text', 'rating']
