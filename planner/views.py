# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from planner.models import Client
from planner.forms import ClientForm


@login_required
def index(request):
    return render(request, "planner/index.html", {
        'title': 'Home',
        'active': 'visits'
    })


@login_required
def clients(request):
    return render(request, "planner/clients.html", {
        'title': 'Clients',
        'active': 'clients',
        'clients': Client.objects.all(),
        'client_form': ClientForm
    })


@login_required
def doctors(request):
    return render(request, "planner/doctors.html", {
        'title': 'Doctors',
        'active': 'doctors'
    })


@login_required
def problems(request):
    return render(request, "planner/problems.html", {
        'title': 'Problems',
        'active': 'problems'
    })
