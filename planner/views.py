# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, "planner/index.html", {
        'title': 'Home'
    })
