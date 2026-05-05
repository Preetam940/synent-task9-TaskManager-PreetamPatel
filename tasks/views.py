import re
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import User
from .models import TasksModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout


def dashboard(req):
        tasks = None
        if req.user.is_authenticated:    
          tasks = TasksModel.objects.filter(user = req.user)
        return render(req,"tasks/dashboard.html",{"tasks":tasks})

@login_required
def add_task(req):
    if req.method == "POST":
        title = req.POST.get('title')
        description = req.POST.get('Description')
        
        TasksModel.objects.create(user = req.user,
                                  title = title,
                                  Description = description)
        return redirect('dashboard')
    
    return render(req,"tasks/add-task.html")

@login_required
def delete_task(req, id):
    task = get_object_or_404(TasksModel,id = id, user=req.user)
    task.delete()
    return redirect('dashboard')

@login_required
def edit_task(req, id):
    task = get_object_or_404(TasksModel, id=id,user= req.user)
    if req.method == "POST":
        task.title = req.POST.get('title')
        task.Description = req.POST.get('Description')
        task.save()
        return redirect('dashboard')
    return render(req, "tasks/edit-task.html",{"task":task})

def user_login(req):
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req,username = username, password = password)
        
        if user is not None:
            login(req, user)
            return redirect('dashboard')
        else:
            messages.error(req,"Invalid credentials")
    return render(req, "tasks/login.html")

def register(req):
    if req.method == "POST":
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')
        
        if len(username) < 3:
            messages.error(req,"Username must be at least 3 characters")
            return redirect('register')
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern,email):
            messages.error(req,"Invalid email format")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(req, "Passwords do not match")
            return redirect('register')
        
        if len(password) < 6:
            messages.error(req,"Password too short")
            return redirect('register')
        
        if User.objects.filter(username = username).exists():
            messages.error(req, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(username = username ,  email = email , password = password)
        user.save()
        
        messages.success(req, "Registration Successful")
        return redirect('login')
            
        
    return render(req, "tasks/register.html")

def user_logout(req):
    logout(req)
    return render(req,'tasks/logout.html')

