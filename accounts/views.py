from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from planner.forms import SinginForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from accounts.forms import ProfileForm


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
    return redirect('/')


@login_required
def profiles(request, profile_edit_id=None, profile_remove_id=None):
    """
    The doctors view
    """

    if profile_remove_id:
        profile = Profile.objects.get(id=profile_remove_id)
        profile.delete()
        return redirect('/accounts/')
    elif profile_edit_id:
        profile = Profile.objects.get(id=profile_edit_id)
        profile_form = ProfileForm(initial={
            'id': profile.id,
            'username': profile.user.username,
            'email': profile.user.email
        })
        profile_form.helper.form_action = '/accounts/'
        profile_form.helper.form_id = 'account-edit-form'
        return render(request, "planner/profiles/edit.html", {
            'profile_form': profile_form,
            'profile_edit_id': profile_edit_id,
            'is_register': request.user.groups.filter(name='Registers'),
        })

    profiles_list = Profile.objects.are_doctors()
    paginator = Paginator(profiles_list, 25)  # 25 items per page

    page = request.GET.get('page')
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return render(request, "planner/profiles/index.html", {
        'title': 'Doctors',
        'active': 'Doctors',
        'is_register': request.user.groups.filter(name='Registers'),
        'profiles': profiles,
        'profile_form': ProfileForm
    })
