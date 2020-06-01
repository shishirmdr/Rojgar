from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User


def home(request):
    return render(request,"home.html")


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('results')
            except IntegrityError:
                return render(request, 'signup.html',
                {'form': UserCreationForm, 'error': 'the username has already been used'})
        else:
            return render(request, 'signup.html',
                          {'form': UserCreationForm, 'error': 'the password did not match'})


def loginuser(request):
    if request.method=="GET":
        return render(request,"login.html",{'form':AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,"login.html",{'form':AuthenticationForm,'error':"the username and the password dint match"})
        else:
            login(request,user)
            return redirect("results")


def logoutuser(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')


def results(request):
    return render(request,'results.html')
