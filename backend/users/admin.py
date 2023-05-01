from django.contrib import admin
from django.contrib.admin import register

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'email')
    empty_value_display = '===пусто==='
