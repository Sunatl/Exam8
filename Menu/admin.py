from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Borrow)
admin.site.register(Review)
admin.site.register(Genre)