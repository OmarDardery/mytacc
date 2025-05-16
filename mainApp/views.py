from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.middleware import csrf
from .models import User, Task, Debt
import random
import string
import json
from django.conf import settings
from google import genai
from pydantic import BaseModel

class Task_Point(BaseModel):
    appropriate: bool
    points: int
    cleaned_text: str

class Debt_Point(BaseModel):
    appropriate: bool
    points: int
    cleaned_text: str
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
def get_user(request):
    if request.method == 'GET':
        user = request.user
        user_data = {
            'username': user.username,
            'email': user.email,
            'points': user.points
        }
        return JsonResponse(user_data)
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

@login_required(login_url='')
def add(request, type):
    if request.method == 'POST':
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        data = json.loads(request.body)
        if type == 'task':
            name = data.get('name')
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"This is a task assessment for a user, they submitted this task to show their gratitude, first determine whether what was submitted is inappropriate or shouldn't be counted as task or is valid, then assess it on a scale from 1 to 100 points based on how meaningful or impactful it is for a community, example task: donate 10 dollars to charity. if the user submitted nothing or something that cannot be understood, return inappropriate. The user submitted: '{name}'",
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Task_Point,
                },
            )
            response = response.parsed
            if response.appropriate:
                user = request.user
                task = Task(name=name, user=user, points=response.points)
                task.save()
                return JsonResponse({'status': 'success', 'message': 'added task successfully'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Task is inappropriate'})
        elif type == 'debt':
            name = data.get('name')
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"This is a system that translates things that a user says they are grateful for into debt, by rating things from 0 to 100 based on how much the user should be grateful for it. first assess whether the user is being serious and set the 'appropriate attribute accordingly. then asses it and put the score in points. The user submitted: '{name}'",
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Debt_Point,
                },
            )
            response = response.parsed
            if response.appropriate == True:
                user = request.user
                debt = Debt(name=name, user=user, points=response.points)
                debt.save()
                return JsonResponse({'status': 'success', 'message': 'added debt successfully'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Debt is inappropriate'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

@login_required(login_url='')
def get_tasks_and_debts_and_points(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        debts = Debt.objects.filter(user=request.user)
        tasks_data = [{'name': task.name, 'points': task.points, "id": task.id, "done": task.completed} for task in tasks]
        debts_data = [{'name': debt.name, 'points': debt.points, "id": debt.id, "paid": debt.paid} for debt in debts]
        return JsonResponse({'tasks': tasks_data, 'debts': debts_data, 'points': request.user.points})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

@login_required(login_url='')
def delete_task(request, id):
    if request.method == 'DELETE':
        task = Task.objects.filter(id=id, user=request.user).first()
        if task:
            task.delete()
            return JsonResponse({'status': 'success', 'message': 'Task deleted successfully'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Task not found'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

@login_required(login_url='')
def task_is_done(request, id):
    if request.method == 'UPDATE':
        task = Task.objects.filter(id=id, user=request.user).first()

        if task:
            task.completed = True
            task.save()
            request.user.points += task.points
            request.user.save()
            return JsonResponse({'status': 'success', 'message': 'Debt deleted successfully'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Debt not found'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

@login_required(login_url='')
def pay_off_debt(request, id):
    if request.method == 'UPDATE':
        debt = Debt.objects.filter(id=id, user=request.user).first()
        if debt:
            request.user.points -= debt.points
            debt.paid = True
            debt.save()
            request.user.save()
            return JsonResponse({'status': 'success', 'message': 'Debt deleted successfully'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Debt not found'})
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

def send_home(request):
    if request.method == 'GET':
        return redirect("home")
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})