from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render

from app.models import CustomUser
from app.forms import MyAuthenticationForm, RegistrationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect

@csrf_protect

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. This is the index file.")
    if request.user.is_authenticated:
        if request.user.state == "Step 1":
            return render(request, 'step1.html', context={'user':request.user}) # will add step1Form
        elif request.user.state == "Step 2":
            return render(request, 'step2.html', context={'user':request.user}) # will add step2Form
        elif request.user.state == "Step 3":
            return render(request, 'step3.html', context={'user':request.user}) # will add step3Form
        return render(request, 'index.html', context={'user':request.user})
    
    form = MyAuthenticationForm(request.POST or None)
    return render(request, 'login.html', {'form': form, 'error': 'sample'})

def auth_login(request):
    if request.method == 'POST':
        form = MyAuthenticationForm(request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')                        
                return redirect('index')
            
    return render(request, 'login.html', {'error': 'Wrong credentials', 'form': MyAuthenticationForm()})

def registerUser(request):
    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)

        if form.is_valid():

            # Saving user to the database
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()

            # Automatically signing the user up
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('index')

    else:
        form = RegistrationForm()

    return render(request, 'registration/login.html', {'form': form})

def registerView(request):
    return render(request, 'reg.html', context={})
def step1View(request):
    pass

def step2View(request):
    pass

def step3View(request):
    pass

