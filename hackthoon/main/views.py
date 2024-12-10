from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as user_login, logout
from .models import CustomUser, UserProfile, DayVisit, AttendanceRecord
from .forms import UserProfileForm, CustomUserCreationForm
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def search_users(request):
    # Получаем все записи из модели CustomUser
    users = CustomUser.objects.all()

    # Получаем параметры из GET-запроса
    fio = request.GET.get('fio', '').strip().lower()
    group = request.GET.get('group', '').strip()
    course = request.GET.get('course', '').strip()
    absent_count = request.GET.get('absent_count', '').strip()

    if fio:
        users = users.filter(Fio__icontains=fio)  # Фильтрация по имени (ФИО)

    if group:
        users = users.filter(group__title__icontains=group)  # Фильтрация по группе

    if course:
        users = users.filter(group__course__icontains=course)  # Фильтрация по курсу
    if absent_count:
        users = users.filter(group__course__icontains=absent_count)  # Фильтрация по курсу

    # Рендерим результаты в шаблон
    return render(request, 'main/user.html', {'users': users})


def view_profile(request):

    user = request.user

    return render(request, 'accounts/profile.html', {
        'user': user,
    })



def home(request):
    users = CustomUser.objects.all()
    return render(request, 'main/user.html', {'users': users})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            return HttpResponseRedirect('../')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'auth/login.html')

def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
        else:
            return render(request, 'accounts/edit_profile.html', {'form': form, 'error': 'Form is not valid'})

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')