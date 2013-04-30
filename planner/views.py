# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from planner.models import Client
from planner.forms import ClientForm
from django.contrib.auth.models import User


@login_required
def index(request):
    return render(request, "planner/index.html", {
        'title': 'Home',
        'active': 'visits'
    })


@login_required
def clients(request):
    return render(request, "planner/clients/index.html", {
        'title': 'Clients',
        'active': 'clients',
        'clients': Client.objects.all(),
        'client_form': ClientForm
    })


def clients_rest(request):
    if request.method == 'GET':
        return None
    elif request.method == 'POST':
        return None
    elif request.method == 'PUT':
        return None
    elif request.method == 'DELETE':
        return None


@login_required
def doctors(request):
    doctors_list = User.objects.filter(groups__name='Doctors')
    return render(request, "planner/doctors/index.html", {
        'title': 'Doctors',
        'active': 'doctors',
        'list': doctors_list
    })


@login_required
def problems(request):
    return render(request, "planner/problems/index.html", {
        'title': 'Problems',
        'active': 'problems'
    })
