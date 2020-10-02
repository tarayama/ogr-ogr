from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'home.html')

# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
                    signup_form.save()
                    username = signup_form.cleaned_data.get('username')
                    password = signup_form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('top', request.user)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
