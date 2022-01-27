from django.http import HttpResponse
from django.shortcuts import render

from app.models import CustomUser

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. This is the index file.")
    if request.user.is_authenticated:
        if request.user.state == "Step 1":
            return render(request, 'step1.html', context={})
        elif request.user.state == "Step 2":
            return render(request, 'step2.html', context={})
        elif request.user.state == "Step 3":
            return render(request, 'step3.html', context={})
        return render(request, 'index.html', context={})
    
    return render(request, 'reg.html', context={})

def loginView(request):
    return render(request, 'login.html', context={})
def step1View(request):
    pass

def step2View(request):
    pass

def step3View(request):
    pass

