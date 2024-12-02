from django.urls import path
from .views import *
urlpatterns = [
    # Base page
    path('Home', Base.as_view(), name='base'),
    path("",login,name="login"),
    path('accounts/logout/', user_logout, name='logout'),

    
]