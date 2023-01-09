# from django.contrib import admin
# from .models import *

# # Register your models here.
# admin.site.register(QuesModel)

from django.contrib import admin
from .models import Category, Question
# Register your models here.


admin.site.register(Category)
admin.site.register(Question)