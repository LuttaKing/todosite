from audioop import reverse
import email
from email import message
import threading
from django.shortcuts import render,redirect
from django.contrib import messages 
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from helpers.decoratoz import block_authed_user
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError #force_text
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user,request):
    current_site = get_current_site(request)
    email_subject = "Activate account"
    email_body = render_to_string('authentication/activate.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user),
    })

    email=EmailMessage(subject=email_subject,body=email_body,from_email=settings.EMAIL_FROM_USER,to=[user.email])
    # email.send() no thread, use next
    EmailThread(email).start()


@block_authed_user
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
            return render(request,'authentication/register.html',context, status=409)

        if context["has_error"]:
            return render(request,'authentication/register.html',context)

        user = User.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.save()

        # send_activation_email(user,request)


        messages.add_message(request,messages.SUCCESS, f"Account created for {email}, Check inbox for activation link")
        return redirect('login')


    return render(request,'authentication/register.html')

@block_authed_user
def login_user(request):
    if request.method =="POST":
        context={'has_error':False,'data':request.POST}
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        # if not user.is_email_verified:
        #     messages.add_message(request,messages.ERROR, "Email not verified")
        #     return render(request,'authentication/login.html',context)

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


def activate_user(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)


    except Exception as e:
        user=None

    if user and generate_token.check_token(user,token):
        user.is_email_verified=True
        user.save()

        messages.add_message(request,messages.SUCCESS, f"Activated {user.username}")
        return redirect(reverse('login'))

    return render(request,'authentication/activate_failed.html',{'user':user})
