from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request,f'you are now logges as {username}')
                return redirect('home')  # Redirect to home page after successful login
            else:
                # This case is actually handled by the form's internal validation, so no need to handle it manually.
                messages.error(request,f'unable to login')
        else:
            messages.error(request,f'unable to login')
        # If form is not valid, or credentials are wrong, re-render the form with errors
        return render(request, 'views/login.html', {'login_form': login_form})

    else:  # For a GET request
        login_form = AuthenticationForm()
        return render(request, 'views/login.html', {'login_form': login_form})

def register_view(request):
    register_form=UserCreationForm()
    return render(request,'views/register.html',{'register_form':register_form})