from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from django.contrib.auth import login as django_login

def singup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(settings.LOGOUT_REDIRECT_URL)
    
    # else:
    #     form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        # 내가 작성한 코드
        # form(request, request.user())
        # form.session()
        # response = 
        # response.redirect(request, settings.LOGIN_REDIRECT_URL)
        # return response

        django_login(request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL)
    
    # else:
    #     form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)

