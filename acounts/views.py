from Menu.forms import CustomUserForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class Singup(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/singup.html" 