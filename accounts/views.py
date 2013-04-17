from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from planner.forms import SinginForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


def account_login(request):
    """
    This is the login
    """
    if request.method == 'POST':
        form = SinginForm(request.POST)
        if form.is_valid():
            """
            Form is valid, proceed to check logins
            """
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    form.add_form_error('Disabled account')
            else:
                form.add_form_error('Invalid login')
        else:
            form.add_form_error('Not valid data')

    else:
        form = SinginForm()
    return render(request, "planner/singin.html", {
        'form': form
    })


def account_logout(request):
    logout(request)
