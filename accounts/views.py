from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .models import CustomUser


def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            error = "Invalid email or password"

    return render(request, "accounts/login.html", {"error": error})


def register_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            error = "Passwords do not match"
        elif CustomUser.objects.filter(email=email).exists():
            error = "Email already registered"
        else:
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            return redirect("home")

    return render(request, "accounts/register.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("home")
