# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from planner.models import Client
from planner.models import Problem
from planner.models import Pet
from planner.models import Visit
from planner.models import Schedule
from planner.forms import ClientForm
from planner.forms import PetForm
from planner.forms import ProblemForm
from planner.forms import VisitForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.utils import timezone


@login_required
def index(request):
    works_today = Schedule.objects.works_today()
    current_time = timezone.now()
    all_works = Schedule.objects.all()

    return render(request, "planner/index.html", {
        'title': 'Home',
        'active': 'overview',
        'works_today': works_today,
        'all_works': all_works,
        'current_time': current_time
    })


@login_required
def clients(request, client_edit_id=None, client_remove_id=None):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client = Client
            try:
                client = Client.objects.get(id=client_edit_id)
            except client.DoesNotExists:
                return redirect('/clients/')

            client.first_name = client_form.cleaned_data['first_name']
            client.last_name = client_form.cleaned_data['last_name']
            client.telephone = client_form.cleaned_data['telephone']
            client.save()
            return redirect('/clients/')
        else:
            return render(request, "planner/clients/edit.html", {
                'client_form': client_form,
                'client_edit_id': client_edit_id,
                'pets': Pet.objects.filter(client=Client.objects.get(id=client_edit_id))
            })

    if client_remove_id:
        client = Client.objects.get(id=client_remove_id)
        client.delete()
        return redirect('/clients/')
    elif client_edit_id:
        return render(request, "planner/clients/edit.html", {
            'client_form': ClientForm(
                Client.objects.values().get(id=client_edit_id)),
            'client_edit_id': client_edit_id,
            'pets': Pet.objects.filter(client=Client.objects.get(id=client_edit_id))
        })

    # Default list view
    client_list = Client.objects.all()
    paginator = Paginator(client_list, 25)  # 25 elements per page

    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, "planner/clients/index.html", {
        'title': 'Clients',
        'active': 'clients',
        'clients': clients,
        'client_form': ClientForm
    })


@login_required
def pets(request, pet_edit_id=None, pet_remove_id=None):
    if request.method == 'POST':
        pet_form = PetForm(request.POST)
        if pet_form.is_valid():
            pet = Pet
            try:
                pet = Pet.objects.get(id=pet_edit_id)
            except pet.DoesNotExists:
                return redirect('/pets/')

            pet.name = pet_form.cleaned_data['name']
            pet.save()
            return redirect('/pets/')
        else:
            return render(request, "planner/pets/edit.html", {
                'pet_form': pet_form,
                'pet_edit_id': pet_edit_id
            })

    if pet_remove_id:
        pet = Pet.objects.get(id=pet_remove_id)
        pet.delete()
        return redirect('/pets/')
    elif pet_edit_id:
        return render(request, "planner/pets/edit.html", {
            'pet_form': PetForm(
                Pet.objects.values().get(id=pet_edit_id)),
            'pet_edit_id': pet_edit_id
        })

    # This is the default list view
    pets_list = Pet.objects.all()
    paginator = Paginator(pets_list, 25)  # 25 Items per page

    page = request.GET.get('page')
    try:
        pets = paginator.page(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
    except EmptyPage:
        pets = paginator.page(paginator.num_pages)

    return render(request, "planner/pets/index.html", {
        'title': 'Pets',
        'active': 'pets',
        'pets': pets,
        'pet_form': PetForm
    })


@login_required
def doctors(request):
    doctors_list = User.objects.filter(groups__name='Doctors')
    return render(request, "planner/doctors/index.html", {
        'title': 'Doctors',
        'active': 'doctors',
        'doctors': doctors_list
    })


@login_required
def problems(request, problem_edit_id=None, problem_remove_id=None):
    if request.method == 'POST':
        problem_form = ProblemForm(request.POST)
        if problem_form.is_valid():
            problem = Problem
            try:
                problem = Problem.objects.get(id=problem_edit_id)
            except problem.DoesNotExists:
                return redirect('/problems/')

            problem.name = problem_form.cleaned_data['name']
            problem.code = problem_form.cleaned_data['code']
            problem.color = problem_form.cleaned_data['color']
            problem.save()
            return redirect('/problems/')
        else:
            return render(request, "planner/problems/edit.html", {
                'problem_form': problem_form,
                'problem_edit_id': problem_edit_id
            })

    if problem_remove_id:
        problem = Problem.objects.get(id=problem_remove_id)
        problem.delete()
        return redirect('/problems/')
    elif problem_edit_id:
        return render(request, "planner/problems/edit.html", {
            'problem_form': ProblemForm(
                Problem.objects.values().get(id=problem_edit_id)),
            'problem_edit_id': problem_edit_id
        })

    # This is the default list view
    problems_list = Problem.objects.all()
    paginator = Paginator(problems_list, 25)  # 25 Items per page

    page = request.GET.get('page')
    try:
        problems = paginator.page(page)
    except PageNotAnInteger:
        problems = paginator.page(1)
    except EmptyPage:
        problems = paginator.page(paginator.num_pages)

    return render(request, "planner/problems/index.html", {
        'title': 'Problems',
        'active': 'problems',
        'problems': problems,
        'problem_form': ProblemForm
    })


@login_required
def visits(request, visit_edit_id=None, visit_remove_id=None):
    if request.method == 'POST':
        visit_form = VisitForm(request.POST)
        if visit_form.is_valid():
            visit = Visit
            try:
                visit = Visit.objects.get(id=visit_edit_id)
            except visit.DoesNotExists:
                return redirect('/visits/')

            visit.name = visit_form.cleaned_data['name']
            visit.code = visit_form.cleaned_data['code']
            visit.color = visit_form.cleaned_data['color']
            visit.save()
            return redirect('/visits/')
        else:
            return render(request, "planner/visits/edit.html", {
                'visit_form': visit_form,
                'visit_edit_id': visit_edit_id
            })

    if visit_remove_id:
        visit = Visit.objects.get(id=visit_remove_id)
        visit.delete()
        return redirect('/visits/')
    elif visit_edit_id:
        return render(request, "planner/visits/edit.html", {
            'visit_form': VisitForm(
                Visit.objects.values().get(id=visit_edit_id)),
            'visit_edit_id': visit_edit_id
        })

    # This is the default list view
    visits_list = Visit.objects.all()
    paginator = Paginator(visits_list, 25)  # 25 Items per page

    page = request.GET.get('page')
    try:
        visits = paginator.page(page)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(paginator.num_pages)

    return render(request, "planner/visits/index.html", {
        'title': 'visits',
        'active': 'visits',
        'visits': visits,
        'visit_form': VisitForm
    })
