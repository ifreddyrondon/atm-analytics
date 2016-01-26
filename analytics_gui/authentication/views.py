# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View

from analytics_gui.authentication.forms import CustomAuthenticationForm


class Login(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, 'authentication/login.html', {
            'form': form
        })

    @staticmethod
    def post(request, *args, **kwargs):
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, "Usuario o Contraseña incorrecto")
                return render(request, 'authentication/login.html', {
                    'form': form
                })
            if not user.is_active:
                messages.info(request, "Usuario inactivo")
                return render(request, 'authentication/login.html', {
                    'form': form
                })

            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            login(request, user)
            return redirect('/')

        return render(request, 'authentication/login.html', {
            'form': form
        })


class Logout(View):
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return redirect('/')
