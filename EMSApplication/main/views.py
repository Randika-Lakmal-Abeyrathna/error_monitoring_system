from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import LogPath


# Create your views here.
@login_required(login_url='login/')
def index (response):
    if response.user.is_authenticated:
        if response.user.is_superuser:
            return redirect(reverse('adminhome'))
        else:
            configlist = LogPath.objects.all()
            context= {
                'configlist':configlist
            }
            return render(response,"main/home.html",context)

    

def loginUser(response):
    
    if response.user.is_authenticated:
        if response.user.is_superuser:
            return redirect(reverse('adminhome'))
        else:
            return redirect(reverse('home'))
    else: 
        if response.method == "POST":
            username=response.POST.get('username')
            password=response.POST.get('password')
            print(username)
            print(password)
            user = authenticate(response,username=username,password=password)
            print(user)
            if user is not None:
                if user.is_superuser:
                    login(response,user)
                    return redirect(reverse('adminhome'))
                else:
                    login(response,user)
                    return redirect(reverse('home'))


        return render(response,"registration/login.html")

@login_required(login_url='/')
def register(response):
    if response.user.is_authenticated:
        if response.user.is_superuser:
            if response.method == "POST":
                form = RegisterUserForm(response.POST)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('adminhome'))
        
            else:
                form = RegisterUserForm()
    
            return render(response,"main/userregister.html",{"form":form})
        else:
            return redirect(reverse('home'))

    

def reset(response):
    return render(response,"main/resetpassword.html")


@login_required(login_url='/')
def adminhome(response):

    configlist = LogPath.objects.all()

    user = get_user_model()
    users = user.objects.all()
    context= {
        'userlist':users,
        'configlist':configlist
    }
    return render(response,"main/adminhome.html",context)


def logoutUser(request):
    logout(request)
    return redirect('login/')

@login_required(login_url='/')
def updateUser(request):
    if request.method == "POST":
            username=request.POST.get('username')
            email=request.POST.get('email')
            userrole=request.POST.get('userrole')
            status =request.POST.get('status') 
            try:
                user = get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                user= None
            
            if user is not None:
                if  request.user == user:
                    print("cannot update loged account")
                else:
                    user.email = email
                    user.is_superuser = userrole
                    user.is_active = status
                    user.save()
    configlist = LogPath.objects.all()
    user = get_user_model()
    users = user.objects.all()
    context= {
        'userlist':users,
        'configlist':configlist
    }
    return redirect(reverse('adminhome'),context)

@login_required(login_url='/')
def addserver(request):
    if request.method == "POST":
        path = request.POST.get('ip')
        print(path)
        try:
            logpath = LogPath.objects.get(path=path)
        except LogPath.DoesNotExist: 
            logpath= None
        print(logpath)
        if logpath is not None:
            print("Path Alrady exsists")
        else:
            newPath= LogPath()
            newPath.path= path
            newPath.enabled =1
            newPath.user_id = request.user

            newPath.save()

    configlist = LogPath.objects.all()
    user = get_user_model()
    users = user.objects.all()
    context= {
        'userlist':users,
        'configlist':configlist
    }
    return redirect(reverse('adminhome'),context)


@login_required(login_url='/')
def updateserver(request):
    if request.method == "POST":
        path = request.POST.get('ip')
        print(path)
        status =request.POST.get('status')
        try:
            logpath = LogPath.objects.get(path=path)
        except LogPath.DoesNotExist: 
            logpath= None
        
        if logpath is not None:
            logpath.enabled=status
            logpath.save()

    configlist = LogPath.objects.all()
    user = get_user_model()
    users = user.objects.all()
    context= {
        'userlist':users,
        'configlist':configlist
    }
    return redirect(reverse('adminhome'),context)