from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home page after successful login
            else:
                # This case is actually handled by the form's internal validation, so no need to handle it manually.
                pass
        
        # If form is not valid, or credentials are wrong, re-render the form with errors
        return render(request, 'views/login.html', {'login_form': login_form})

    else:  # For a GET request
        login_form = AuthenticationForm()
        return render(request, 'views/login.html', {'login_form': login_form})
