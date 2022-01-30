from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render

from app.models import CustomUser
from app.forms import MyAuthenticationForm, RegistrationForm, Step1Form, Step2Form, Step3Form
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect

@csrf_protect

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. This is the index file.")
    if request.user.is_authenticated:
        if request.user.state == "Step 1":
            return render(request, 'step1.html', context={'form':Step1Form()}) # will add step1Form
        elif request.user.state == "Step 2":
            return render(request, 'step2.html', context={'form':Step2Form()}) # will add step2Form
        elif request.user.state == "Step 3":
            return render(request, 'step3.html', context={'form':Step3Form()}) # will add step3Form
        return render(request, 'index.html', {})
    
    form = MyAuthenticationForm(request.POST or None)
    return render(request, 'login.html', {'form': form})

def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')                        
            return redirect('index')
            
    return render(request, 'login.html', {'error': 'Wrong credentials', 'form': MyAuthenticationForm()})

@csrf_protect
def registerView(request):
    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            print('form is valid')

            # Saving user to the database
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()

            # Automatically signing the user up
            raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=user.username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('index')
        return render(request, 'reg.html', {'form': RegistrationForm(), 'error': 'User already exists'})

    else:
        form = RegistrationForm()

    return render(request, 'reg.html', {'form': form})

def step1View(request):
    if request.method == 'POST':
        if 'back1' in request.POST:
            # back1 transition
            pass
        else:
            form = Step1Form(request.POST)
            if form.is_valid():
                user = request.user
                user.submit1(form.cleaned_data['first_name'])
                return render(request, 'step2.html', {'form': Step2Form()})
        
    return redirect('index')

def step2View(request):
    if request.method == 'POST':
        form = Step2Form(request.POST)
        
        if form.is_valid():
            user = request.user
            user.submit2(form.cleaned_data['last_name'])
            return render(request, 'step3.html', {'form': Step2Form()})
        
    return redirect('index')

def step3View(request):
    if request.method == 'POST':
        form = Step3Form(request.POST)
        
        if form.is_valid():
            user = request.user
            user.submit3(form.cleaned_data['email'])
            return redirect('index')
        
    return redirect('index')

def logoutUser(request):
    logout(request)
    return redirect('index')