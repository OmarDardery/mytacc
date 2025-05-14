from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.middleware import csrf
from django.conf import settings
from .models import User, Task, Debt
import random
import string
import json

@login_required(login_url='')
def home(request):
    return render(request, 'mainApp_react/home/build/index.html')
def index(request):
    csrf_token = csrf.get_token(request)
    if request.user.is_authenticated:
        response = redirect(home)
        response.set_cookie('mytacc_csrftoken', csrf_token)
        return response
    else:
        response = render(request, 'mainApp_react/liasu/build/index.html')  # Get the CSRF token for the request
        response.set_cookie('mytacc_csrftoken', csrf_token)  # Set the CSRF token in a cookie
        return response

def validate_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        email = data.get('email')
        if code and email:
            try:
                cached_code = request.session.get('otp_code')
                # Check if the cached code exists and matches the provided code
                if cached_code == code:
                    try:
                        password = data.get('password')
                        username = data.get('username')
                        user = User.objects.create_user(email=email, password=password, username=username)
                        user.save()
                        login(request, user)
                        return JsonResponse({'status': 'success'})
                    except Exception as e:
                        return JsonResponse({'status': 'failed', 'error': str(e)})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'error': str(e)})

        else:
            return JsonResponse({'status': 'failed', 'error': 'Invalid code or email'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

def send_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        if email:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'failed', 'error': 'Email already exists'})
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'failed', 'error': 'Username already exists'})
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            request.session['otp_code'] = code
            request.session['otp_email'] = email
            request.session.set_expiry(300)
            send_mail(
                'Your Verification Code',
                f'Your verification code is {code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': "success"})
        else:
            return JsonResponse({'status' : 'failed','error': 'Email not real'})
    else:
        return JsonResponse({'status':'failed','error': 'Invalid request'})


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'failed', 'error': 'Username does not exist'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Invalid credentials'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

@login_required(login_url='')
def user_logout(request):
    if request.method == 'POST':
        request.session.flush()
        logout(request)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})
@login_required(login_url='')
def account_page(request):
    return render(request, 'mainApp_react/accountPage/build/index.html')

@login_required(login_url='')
def log(request, type):
    if request.method == 'POST':
        if type == 'task':
            data = json.loads(request.body)
            name = data.get('name')
            points = data.get('points')
            user = request.user
            task = Task(name=name, user=user, points=points)
            task.save()
            return JsonResponse({'status': 'success', 'message': 'added task successfully'})
        elif type == 'debt':
            data = json.loads(request.body)
            name = data.get('name')
            amount = data.get('amount')
            user = request.user
            task = Task(name=name, user=user, points=amount)
            task.save()
            return JsonResponse({'status': 'success', 'message': 'added debt successfully'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid type'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})
@login_required(login_url='')
def get_tasks_and_debts(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        debts = Debt.objects.filter(user=request.user)
        tasks_data = [{'name': task.name, 'points': task.points, 'done': task.completed} for task in tasks]
        debts_data = [{'name': debt.name, 'points': debt.points} for debt in debts]
        return JsonResponse({'tasks': tasks_data, 'debts': debts_data})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})