from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Content
import re

# Create your views here.
def home(request):
    para=Content.objects.order_by('?')[:3]
    return render(request, 'home.html', {'para' : para})

def addDatatoBase(request):
    if request.method == 'POST':
        title=request.POST['title']
        subject=request.POST['subject']
        description=request.POST['description']
        Links=request.POST['links']
        author=request.user.username
        Content_data=Content(title=title, subject=subject, description=description, author=author, Links=Links)
        Content_data.save()
    
    return redirect('/')

def EditDatatoBase(request, id):
    if request.method == 'POST':
        Content_data=Content.objects.get(pk=id)
        Content_data.title=request.POST.get('title')
        Content_data.subject=request.POST.get('subject')
        Content_data.description=request.POST['description']
        Content_data.Links=request.POST['links']
        Content_data.save()
    return redirect('/')

def dashboard(request):
    para=Content.objects.filter(author=request.user.username)
    return render(request, 'dashboard.html', {'para' : para})

def disData(request, id):
    para=Content.objects.filter(id=id)
    lin=re.findall("(?P<url>https?://[^\s]+)", para[0].Links)
    nam=re.findall("(::.::)",para[0].Links)
    ulist=para[0].rated.split(',')
    flag=1
    for i in ulist:
        if i==request.user.username:
            flag=0
    return render(request, 'display.html', {'para' : para, 'lin':lin, 'nam':nam, 'flag':flag})

def rate(request, id):
    para=Content.objects.get(pk=id)
    r=int(request.POST.get('rate'))
    para.rated=para.rated+','+request.user.username
    ulist=para.rated.split(',')
    n=len(ulist)-1
    print(request.user.username)
    para.rate=(para.rate+r)/n
    para.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteData(request, id):
    para=Content.objects.filter(id=id)
    para.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def editData(request, id):
    para=Content.objects.filter(id=id)
    return render(request, 'EditData.html', {'para' : para})

def addData(request):
    return render(request, 'Enter_Content.html')

def about(request):
    return render(request, 'About.html')

def contact(request):
    return render(request, 'contact.html')

def search(request):
    search_key=request.POST['search_key']
    try:
        para=Content.objects.filter(title__icontains=search_key)
    except Content.DoesNotExist:
        para=None
    return render(request, 'search.html', {'para' : para})

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "userame already exists, try with some other name")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already exists, try with some other email")
                return redirect('register')
            else:           
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registered successfully, now login to website")
                return redirect('login')
        else:
            messages.error(request, "!!passwords dont match, try agan.")
            return redirect('register')

    else:
        return render(request, 'login.html')


def Login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')
        
    else:
        return render(request, 'login.html')

def Logout(request):
    auth.logout(request)
    return redirect('/')
