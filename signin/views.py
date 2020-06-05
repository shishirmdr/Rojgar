from .forms import RegistrationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required



def signup(request):
    template = 'accounts/signup.html'

    if request.method == 'GET':
        return render(request, template, {'form': RegistrationForm})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'],
                            password=request.POST['password1'],
                            email=request.POST['email'])
                            # first_name=request.POST['first_name'],last_name= request.POST['last_name'])
                    user.save()
                    login(request, user)
                    return redirect('dashboard')
                except IntegrityError:
                    return render(request, template, {'form': RegistrationForm,
                                                      'error': 'the username has already been used'})
            else:
                return render(request, template, {'form': RegistrationForm,
                                                  'error': 'the password did not match'})
        except ValueError:
            return render(request, template, {'form': RegistrationForm,
                                              'error': 'Please enter valid data'})

def loginuser(request):
    template = "accounts/login.html"

    if request.method=="GET":
        return render(request, template,{'form':AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, template, {
                'form':AuthenticationForm,
                'error':"the username and the password didn't match"
            })
        else:
            login(request, user)

            if "next" in request.GET:
                return redirect(request.GET['next'])
            return redirect("dashboard")


@login_required
def logoutuser(request):
    if request.method =="POST":
        logout(request)

    return redirect('home')
