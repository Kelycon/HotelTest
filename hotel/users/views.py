# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    LoginForm, UserCreationForm
)


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_auth = form.cleaned_data
            user = authenticate(request,  username=user_auth['username'],  password=user_auth['password'])
            if user is not None:
                if user.is_active:
                    request.session.flush()
                    login(request, user)
                    previous_url = request.POST.get('previous_url')

                    if previous_url:
                        return redirect(previous_url)

                    return render(request, 'home.html')
                else:
                    return render(request, 'signin.html', {'error': 'Cuenta inactiva'})
            else:
                return render(request, 'signin.html', {'error': 'Usuario o contraseña invalidos.'})
    else:
        form = LoginForm()
        return render(request, 'signin.html', {'form': form})


@login_required
def signout(request):
    if request.user.is_authenticated:
        request.session.flush()
        logout(request)

    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
