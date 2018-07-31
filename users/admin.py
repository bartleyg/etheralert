from django.contrib import admin
from django.contrib.auth import get_user_model

admin.register(get_user_model(), admin.ModelAdmin)
