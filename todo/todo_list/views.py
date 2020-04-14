from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import List
from .forms import ListForm
from .forms import SignUpForm
from .forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login_user(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are successfully Logged In!"))
            return redirect('todohome')
        else:
            messages.success(request, ("Error Logging In, Please Try Again..."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out!"))
    return redirect('home')

def register_user(request):
    if request.method== 'POST':
        form =  SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have Been Registered Successfully!!"))
            return redirect('todohome')
    else:
        form =  SignUpForm()
    context={'form':form}
    return render(request, 'register.html', context)

def edit_profile(request):
    if request.method== 'POST':
        form =  EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("You Have Edited Your Profile Successfully!!"))
            return redirect('todohome')
    else:
        form =  EditProfileForm(instance=request.user)
    context={'form':form}

    return render(request, 'edit_profile.html', context)

def change_password(request):
    if request.method== 'POST':
        form =  PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("You Have Edited Your Password Successfully!!"))
            return redirect('todohome')
    else:
        form =  PasswordChangeForm(user=request.user)
    context={'form':form}

    return render(request, 'change_password.html', context)




def todohome(request):
    if request.method == "POST":
        form = ListForm(request.POST or None)
        all_items = List.objects.filter(user=request.user)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user = request.user
            obj.save()
            messages.success(request, ("Item Has Been Added To List!"))
            return render(request, "todohome.html", {"all_items":all_items})
    else:
        form = ListForm()
        all_items = List.objects.filter(user=request.user)
        return render(request, "todohome.html", {"all_items":all_items})

def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ("Item Has Been Deleted"))
    return redirect('todohome')

def cross_off(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('todohome')

def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('todohome')

def edit(request, list_id):
    if request.method == "POST":
        item = List.objects.get(pk=list_id)
        form = ListForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, ("Item Has Been Edited!"))
            return redirect('todohome')
        else:
            messages.success(request, ("Item can't be empty"))
            return render(request, "edit.html", {"item":item})
    else:
        item = List.objects.get(pk=list_id)
        return render(request, "edit.html", {"item":item})
