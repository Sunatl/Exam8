from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
@login_required
def user_logout(request):
    logout(request) 
    return render(request, 'registration/log_out.html') 

def login(request):
    return redirect("accounts/login/")


class Base(TemplateView):
    template_name = "base.html"