from django.urls import reverse_lazy
from .models import Grade, Wallet, Book, Purchase,CustomUser
from .forms import GradeForm, WalletForm, BookForm, PurchaseForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# User logout
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/log_out.html')


# Redirect to login page
def login(request):
    return redirect("accounts/login/")


# Base and Home pages
class Base(TemplateView):
    template_name = "base.html"


class Home(TemplateView):
    template_name = "home.html"


# CRUD for Grade
class GradeListView(ListView):
    model = Grade
    template_name = 'genre_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        queryset = Grade.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset


class GradeDetailView(DetailView):
    model = Grade
    template_name = 'genre_detail.html'
    context_object_name = 'grade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grade = self.get_object()  # Get the current Grade object

        # Filter students who belong to this grade
        students = CustomUser.objects.filter(grade=grade)

        # Now, filter Wallet objects for each student using a relationship with CustomUser
        wallets = Wallet.objects.filter(student__in=students)  # Filter Wallets related to the students

        context['wallets'] = wallets  # Add the Wallets to the context
        context['students'] = students  # Add the students to the context
        context['total_students'] = students.count()  # Add the total number of students

        return context




class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'genre_form.html'
    success_url = reverse_lazy('grade-list')

    def test_func(self):
        # Only allow staff members to create grades
        return self.request.user.is_staff


class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'genre_form.html'
    success_url = reverse_lazy('grade-list')

    def test_func(self):
        # Only allow staff members to update grades
        return self.request.user.is_staff


class GradeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Grade
    template_name = 'genre_confirm_delete.html'
    success_url = reverse_lazy('grade-list')

    def test_func(self):
        # Only allow staff members to delete grades
        return self.request.user.is_staff


# CRUD for Book
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()  # Get the current book object
        
        grade = book.grade  # Get the grade associated with the current book
        
        # Handle the case where grade is None (book might not be assigned to any grade)
        if grade:
            students = CustomUser.objects.filter(grade=grade)
            grade_name = grade.name  # Name of the grade
        else:
            students = []  # No students to show
            grade_name = "No grade assigned"
        
        # Get wallet information for each student in the grade (whether they owe money)
        student_wallets = {student: Wallet.objects.filter(student=student).first() for student in students}
        
        # Add the students, wallet information, and other relevant data to the context
        context['students_in_grade'] = students
        context['student_wallets'] = student_wallets  # Wallet information for each student
        context['grade_name'] = grade_name  # Add the grade name to the context

        return context






class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Only allow staff members to create books
        return self.request.user.is_staff


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Only allow staff members to update books
        return self.request.user.is_staff


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Only allow staff members to delete books
        return self.request.user.is_staff


# CRUD for Purchase
class PurchaseListView(ListView):
    model = Purchase
    template_name = 'review_list.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        queryset = Purchase.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(book__title__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(review__icontains=search_query)
            )
        return queryset


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = 'review_detail.html'
    context_object_name = 'purchase'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["student"] = Purchase.objects.filter(book = self.kwargs['pk'])
        return context

    

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('purchase-list')

    def form_valid(self, form):
        form.instance.student = self.request.user  # Automatically set the student to the logged-in user
        form.instance.make_purchase()  # Call any additional logic related to making a purchase
        return super().form_valid(form)


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('purchase-list')


class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('purchase-list')


# CRUD for Wallet
class WalletListView(ListView):
    model = Wallet
    template_name = 'borrow_list.html'
    context_object_name = 'wallets'

    def get_queryset(self):
        queryset = Wallet.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(book__title__icontains=search_query)
            )
        return queryset


class WalletDetailView(DetailView):
    model = Wallet
    template_name = 'borrow_detail.html'
    context_object_name = 'wallet'

    def get_object(self):
        # Get the wallet object only if the user has made a purchase
        wallet = get_object_or_404(Wallet, pk=self.kwargs['pk'], user=self.request.user)
        if not self.request.user.purchase_set.exists():
            raise PermissionDenied("You must make a purchase to view your wallet.")
        return wallet



class WalletUpdateView(LoginRequiredMixin, UpdateView):
    model = Wallet
    form_class = WalletForm
    template_name = 'borrow_form.html'
    success_url = reverse_lazy('wallet-list')
    
    
    
    
    
    
    
    
    
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Payment, Purchase
from .forms import PaymentForm

# CRUD for Payment
class PaymentListView(ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        queryset = Payment.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(student__username__icontains=search_query) |
                Q(purchase__book__title__icontains=search_query) |
                Q(payment_method__icontains=search_query)
            )
        return queryset


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment-list')

    def form_valid(self, form):
        form.instance.student = self.request.user  
        if form.instance.status == 'completed':
            pass
        return super().form_valid(form)
