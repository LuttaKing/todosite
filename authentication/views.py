from audioop import reverse
from django.shortcuts import render,redirect
from django.contrib import messages 
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from helpers.decoratoz import authed_user_block


@authed_user_block
def register(request):
    if request.method =="POST":
        context={'has_error':False,'data':request.POST}
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if len(password)<6 or password!= password2:
            messages.add_message(request,messages.ERROR, "Password error")
            context["has_error"] = True

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.add_message(request,messages.ERROR, "Username/email is taken")
            context["has_error"] = True

        if context["has_error"]:
            return render(request,'authentication/register.html',context)

        user = User.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.save()
        messages.add_message(request,messages.SUCCESS, f"Account created for {email}, you can log in")
        return redirect('login')


    return render(request,'authentication/register.html')

@authed_user_block
def login_user(request):
    if request.method =="POST":
        context={'has_error':False,'data':request.POST}
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if not user:
            messages.add_message(request,messages.ERROR, "Login Errorfound")
            return render(request,'authentication/login.html',context)

        login(request,user)
        messages.add_message(request,messages.SUCCESS, f"Welcome {user.username}")
        return redirect(reverse('home'))

    return render(request,'authentication/login.html')

def logout_user(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS, "Loggout success")
    return redirect(reverse('login'))


