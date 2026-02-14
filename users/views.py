from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        login_value = request.POST.get("login")
        password = request.POST.get("password")

        user = authenticate(request, login=login_value, password=password)

        if user is None:
            messages.error(request, "Login ou mot de passe incorrect.")
            return render(request, "login.html")

        login(request, user)

        # Redirection selon rôle
        if user.role == "TABLE":
            return redirect("/")
        elif user.role == "SERVEUR":
            return redirect("/serveur/")
        elif user.role == "CUISINE":
            return redirect("/cuisine/")
        else:
            return redirect("/admin/")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")
