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
from .mainlogic import minlogic
from django.contrib import messages
from datetime import date
from dateutil.relativedelta import relativedelta
import xlsxwriter


# Create your views here.
@login_required(login_url='login/')
def index (request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(reverse('adminhome'))
        else:
            if request.method == "POST":
                fromdate = request.POST.get('fromdate')
                todate  = request.POST.get('todate')
                serverid = request.POST.get('serverid')

                if fromdate =='':
                    fromdate=date.today().strftime("%Y-%m-%d")
                if todate =='':
                    todate = date.today().strftime("%Y-%m-%d")
                serverips =[]
                if serverid == '0':
                    serverips = LogPath.objects.filter(enabled =True)
                else:
                    serverips=LogPath.objects.get(id=serverid)
                
                if 'export' in request.POST:
                    error_list =minlogic.readfillelist(fromdate,todate,serverips,serverid)
                    if len(error_list) >0:
                        minlogic.exportFile(error_list)
                        messages.success(request,"File Exported")
                    else:
                        messages.error(request,"No Data to Export")
                    configlist = LogPath.objects.filter(enabled =True)
                    context= {
                        'configlist':configlist,
                        'error_list':error_list,
                        'fromdate':fromdate,
                        'todate':todate
                    }
                    
                    return render(request,"main/home.html",context)
                else:
                    error_list =minlogic.readfillelist(fromdate,todate,serverips,serverid)
                    configlist = LogPath.objects.filter(enabled =True)
                    context= {
                        'configlist':configlist,
                        'error_list':error_list,
                        'fromdate':fromdate,
                        'todate':todate
                    }
                    
                    return render(request,"main/home.html",context)

            fromdate = (date.today() - relativedelta(months=1)).strftime("%Y-%m-%d")
            todate =date.today().strftime("%Y-%m-%d")
            configlist = LogPath.objects.filter(enabled =True)
            error_list =minlogic.readfillelist(fromdate,todate,configlist,'0')
            # minlogic.exportFile(minlogic,fromdate,todate,configlist,'0')
            context= {
                'configlist':configlist,
                'error_list':error_list,
                'fromdate':fromdate,
                'todate':todate
            }
            return render(request,"main/home.html",context)

    

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
                    messages.success(response,"User registered")
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
                    messages.error(request,"Cannot Update Loged in User")
                else:
                    user.email = email
                    user.is_superuser = userrole
                    user.is_active = status
                    user.save()
                    messages.success(request,"User Updated")
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
        path = path.replace("\\","//")
        print(path)
        try:
            logpath = LogPath.objects.get(path=path)
        except LogPath.DoesNotExist: 
            logpath= None
        if logpath is not None:
            messages.error(request,"Path Alrady Exsists")
        else:
            newPath= LogPath()
            newPath.path= path
            newPath.enabled =1
            newPath.user_id = request.user

            newPath.save()
            messages.success(request,"New Ip Added")

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
            messages.success(request,"IP Updated")

    configlist = LogPath.objects.get(enabled =True)
    user = get_user_model()
    users = user.objects.all()
    context= {
        'userlist':users,
        'configlist':configlist
    }
    return redirect(reverse('adminhome'),context)


@login_required(login_url='/')
def sendEmail(request):
    if request.method == "POST":
        emails =request.POST.get('emails')
        content =request.POST.get('content')
        print(emails)
        if emails =='':
            messages.error(request,"Email address Cannot Be empty")
        elif content == '':
            messages.error(request,"Email Content Cannot Be empty")
        else:
            filterEmails = emails.split(',')
            print(filterEmails)
            minlogic.sendEmail(filterEmails,content)
            messages.success(request,"Email Sent")
        
    
    return redirect(reverse('home'))

