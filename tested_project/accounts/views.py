from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required





# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid details')
            return redirect('/login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username takened')
                return redirect('/')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already taken')
                return redirect('/')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                messages.success(request, 'registered successfully. Then please login first!...')
        else:
            messages.info(request, 'password is not match')
            return redirect('/')
        return redirect('/')
    else:
        return render(request, 'registration.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def edit_profile(request):
    if request.method == 'POST':
        print(request.POST)  # Print POST data for debugging
        user = request.user
        user.username = request.POST.get('username', '')  # Use get() method with default value
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('/')
    else:
        return render(request, 'edit_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if user.check_password(old_password) and new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid password or passwords do not match.')
            return redirect('/change_password')
    else:
        return render(request, 'change_password.html')

