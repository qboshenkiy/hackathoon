from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', )
    
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'Fio', 'group', 'role', 'is_active', 'is_staff')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
