# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from planner.models import Client
from planner.models import Problem
from planner.models import Pet
from planner.models import Visit
from planner.models import Schedule
from planner.forms import ClientForm
from planner.forms import PetForm
from planner.forms import ProblemForm
from planner.forms import VisitForm
from planner.forms import ScheduleFrom
from planner import urls
from planner.utils import sliced_time
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Relative Time Delta
import calendar


@login_required
def index(request, view=None, days=None, weeks=None, months=None):
    """
    The main page, depending on the described view

    view:
    - day
    - week
    - month

    days:
    - +1 ahead
    - 0 current
    - -1 before

    weeks:
    - +1 week ahead
    - 0 current
    - -1 week before

    months:
    - +1 month ahead
    - 0 current
    - -1 month before
    """

    available_views = ('days', 'months', 'weeks')

    all_works = Schedule.objects.all()

    """
    Current date
    """
    current_date = timezone.now()

    """
    Checking the date offsets
    """
    if days is not None:
        days = int(days)
        current_date = current_date + timezone.timedelta(days=days)
    else:
        days = 0  # Defines current date

    if weeks is not None:
        weeks = int(weeks)
        current_date = current_date + relativedelta(weeks=weeks)
    else:
        weeks = 0  # Defines current week

    if months is not None:
        months = int(months)
        current_date = current_date + relativedelta(months=months)
    else:
        months = 0  # Defines current month

    """
    Current month operations
    """
    calendar.setfirstweekday(0)
    month_calendar = calendar.monthcalendar(
        year=current_date.year,
        month=current_date.month
    )

    """
    Current week operations
    """
    week_calendar = []
    for week in month_calendar:
        if current_date.day in week:
            week_calendar = week[:]

    for i, day in enumerate(week_calendar):
        if day != 0:
            week_calendar[i] = timezone.datetime(
                year=current_date.year,
                month=current_date.month,
                day=week_calendar[i]
            )

    """
    Making calendar information more use-full
    """
    i = 0
    day = 0
    for i, week in enumerate(month_calendar):
        for j, day in enumerate(week):
            if month_calendar[i][j] != 0:
                month_calendar[i][j] = timezone.datetime(
                    year=current_date.year,
                    month=current_date.month,
                    day=month_calendar[i][j]
                )

    works_on_date = Schedule.objects.works_on_date(current_date)

    visit_form = VisitForm(initial={
        'appointment_by': Profile.objects.get(user__username=request.user).id
    })

    if view not in available_views:
        view = 'days'

    if view == 'days':
        next_date_url = ''.join((urls.days_url, str(days+1)))
        prev_date_url = ''.join((urls.days_url, str(days-1)))
        now_date_url = ''.join((urls.days_url, str(0)))
    elif view == 'weeks':
        next_date_url = ''.join((urls.weeks_url, str(weeks+1)))
        prev_date_url = ''.join((urls.weeks_url, str(weeks-1)))
        now_date_url = ''.join((urls.weeks_url, str(0)))
    elif view == 'months':
        next_date_url = ''.join((urls.months_url, str(months+1)))
        prev_date_url = ''.join((urls.months_url, str(months-1)))
        now_date_url = ''.join((urls.months_url, str(0)))

    template = "".join(("calendar/", view, ".html"))

    sliced_time_current = sliced_time()
    sliced_time_shifted = sliced_time(shift=True)

    return render(request, template, {
        'title': 'Home',
        'active': 'overview',
        'works_today': works_on_date,
        'all_works': all_works,
        'prev_date_url': prev_date_url,
        'now_date_url': now_date_url,
        'next_date_url': next_date_url,
        'current_date': current_date,
        'visit_form': visit_form,
        'current_absolute_date': timezone.now(),
        'month_calendar': month_calendar,
        'week_calendar': week_calendar,
        'is_register': request.user.groups.filter(name='Registers'),
        'sliced_time': zip(sliced_time_current, sliced_time_shifted),
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
                'pets': Pet.objects.filter(
                    client=Client.objects.get(id=client_edit_id)
                )
            })

    if client_remove_id:
        client = Client.objects.get(id=client_remove_id)
        client.delete()
        return redirect('/clients/')
    elif client_edit_id:
        return render(request, "planner/clients/edit.html", {
            'client_form': ClientForm(
                Client.objects.values().get(id=client_edit_id)
            ),
            'client_edit_id': client_edit_id,
            'pets': Pet.objects.filter(
                client=Client.objects.get(id=client_edit_id)
            ),
            'visits': Visit.objects.filter(
                client=Client.objects.get(id=client_edit_id)
            ),
            'is_register': request.user.groups.filter(name='Registers'),
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
        'is_register': request.user.groups.filter(name='Registers'),
        'clients': clients,
        'client_form': ClientForm
    })


@login_required
def schedules(request):
    """
    Schedule front-end manager
    """
    schedules_list = Schedule.objects.all()
    paginator = Paginator(schedules_list, 25)  # 25 Items per page

    page = request.GET.get('page')
    try:
        schedules = paginator.page(page)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    return render(request, "planner/schedules/index.html", {
        'title': 'Schedules',
        'active': 'schedules',
        'is_register': request.user.groups.filter(name='Registers'),
        'schedules': schedules,
        'schedule_form': ScheduleFrom
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
                'pet_edit_id': pet_edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if pet_remove_id:
        pet = Pet.objects.get(id=pet_remove_id)
        pet.delete()
        return redirect('/pets/')
    elif pet_edit_id:
        pet = Pet.objects.get(id=pet_edit_id)
        return render(request, "planner/pets/edit.html", {
            'pet_form': PetForm({
                'name': pet.name,
                'client': pet.client
            }),
            'pet_edit_id': pet_edit_id,
            'is_register': request.user.groups.filter(name='Registers'),
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
        'is_register': request.user.groups.filter(name='Registers'),
        'pets': pets,
        'pet_form': PetForm
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
                'problem_edit_id': problem_edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if problem_remove_id:
        problem = Problem.objects.get(id=problem_remove_id)
        problem.delete()
        return redirect('/problems/')
    elif problem_edit_id:
        return render(request, "planner/problems/edit.html", {
            'problem_form': ProblemForm(
                Problem.objects.values().get(id=problem_edit_id)),
            'problem_edit_id': problem_edit_id,
            'is_register': request.user.groups.filter(name='Registers'),
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
        'is_register': request.user.groups.filter(name='Registers'),
        'problem_form': ProblemForm
    })


@login_required
def visits(request, visit_edit_id=None, visit_remove_id=None):
    if request.method == 'POST':
        visit_form = VisitForm(request.POST)
        if visit_form.is_valid():
            visit = Visit
            try:
                visit = Visit.objects.get(id=visit_form.cleaned_data['id'])
            except visit.DoesNotExist:
                return redirect('/visits/')
            visit.from_date = visit_form.cleaned_data['from_date']
            visit.to_date = visit_form.cleaned_data['to_date']
            visit.client = visit_form.cleaned_data['client']
            visit.pet = visit_form.cleaned_data['pet']
            visit.problem = visit_form.cleaned_data['problem']
            visit.description = visit_form.cleaned_data['description']
            visit.appointment_by = User.objects.get(
                id=visit_form.cleaned_data['appointment_by'].id
            )
            visit.appointment_to = User.objects.get(
                id=visit_form.cleaned_data['appointment_to'].id
            )
            visit.save()
            return redirect('/visits/')
        else:
            return render(request, "planner/visits/edit.html", {
                'visit_form': visit_form,
                'visit_edit_id': visit_edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if visit_remove_id:
        visit = Visit.objects.get(id=visit_remove_id)
        visit.delete()
        return redirect('/visits/')
    elif visit_edit_id:
        visit = Visit.objects.get(id=visit_edit_id)
        visit_form = VisitForm(initial={
            'id': visit.id,
            'from_date': visit.from_date,
            'to_date': visit.to_date,
            'client': visit.client,
            'pet': visit.pet,
            'problem': visit.problem,
            'description': visit.description,
            'appointment_by': visit.appointment_by,
            'appointment_to': visit.appointment_to
        })
        visit_form.helper.form_action = '/visits/'
        visit_form.helper.form_id = 'visit-edit-form'
        return render(request, "planner/visits/edit.html", {
            'visit_form': visit_form,
            'visit_edit_id': visit_edit_id,
            'is_register': request.user.groups.filter(name='Registers'),
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
        'is_register': request.user.groups.filter(name='Registers'),
        'visits': visits,
        'visit_form': VisitForm(initial={
            'appointment_by': Profile.objects.get(
                user__username=request.user
            ).id
        })
    })
