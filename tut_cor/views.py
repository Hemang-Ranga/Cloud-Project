from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
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

