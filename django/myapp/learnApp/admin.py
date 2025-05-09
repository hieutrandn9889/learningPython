from django.contrib import admin
from .models import Course
from .models import price_course

# Register your models here.
admin.site.register(Course)
admin.site.register(price_course)