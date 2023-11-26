'''assigns models to be manipulated by admin'''
from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Blog)
admin.site.register(models.Account)
admin.site.register(models.Subscriber)
