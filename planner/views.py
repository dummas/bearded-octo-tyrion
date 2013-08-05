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
from planner.forms import ScheduleForm
from planner import urls
from planner.utils import sliced_time
from planner.utils import days_of_the_week
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
    week_calendar = days_of_the_week(
        current_date.year, 
        current_date.isocalendar()[1]
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

    form = VisitForm(initial={
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
        'form': form,
        'current_absolute_date': timezone.now(),
        'month_calendar': month_calendar,
        'week_calendar': week_calendar,
        'is_register': request.user.groups.filter(name='Registers'),
        'sliced_time': zip(sliced_time_current, sliced_time_shifted),
    })


@login_required
def clients(request, edit_id=None, remove_id=None):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = Client
            try:
                client = Client.objects.get(id=edit_id)
            except client.DoesNotExist:
                return redirect('/clients/')

            client.first_name = form.cleaned_data['first_name']
            client.last_name = form.cleaned_data['last_name']
            client.telephone = form.cleaned_data['telephone']
            client.save()
            return redirect('/clients/')
        else:
            return render(request, "planner/clients/edit.html", {
                'form': form,
                'edit_id': edit_id,
                'pets': Pet.objects.filter(
                    client=Client.objects.get(id=edit_id)
                )
            })

    if remove_id:
        client = Client.objects.get(id=remove_id)
        client.delete()
        return redirect('/clients/')
    elif edit_id:
        form = ClientForm(
            Client.objects.values().get(id=edit_id)
        )
        form.helper.form_action = '/clients/edit/' + edit_id + '/'
        form.helper.form_id = 'client-edit-form'
        return render(request, "planner/clients/edit.html", {
            'form': form,
            'edit_id': edit_id,
            'pets': Pet.objects.filter(
                client=Client.objects.get(id=edit_id)
            ),
            'visits': Visit.objects.filter(
                client=Client.objects.get(id=edit_id)
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
        'form': ClientForm
    })


@login_required
def schedules(request, edit_id=None, remove_id=None):
    """
    Schedule front-end manager
    """
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = Schedule
            try:
                schedule = Schedule.objects.get(id=edit_id)
            except schedule.DoesNotExist:
                return redirect('/schedules/')
            # Add the fields
            schedule.save()
            return redirect('/schedules/')
        else:
            return render(request, "planner/schedules/edit.html", {
                'form': form,
                'edit_id': edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if remove_id:
        schedule = Schedule.objects.get(id=remove_id)
        schedule.delete()
        return redirect('/schedules/')
    elif edit_id:
        schedule = Schedule.objects.get(id=edit_id)
        form = ScheduleForm({
            'profile': schedule.profile,
            'start': schedule.start,
            'end': schedule.end
        })
        form.helper.form_action = '/schedules/edit/' + edit_id + "/"
        form.helper.form_id = 'schedule-edit-form'
        return render(request, "planner/schedules/edit.html", {
            'form': form,
            'edit_id': edit_id,
            'is_register': request.user.groups.filter(name='Registers'),
        })

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
        'form': ScheduleForm
    })


@login_required
def pets(request, edit_id=None, remove_id=None):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = Pet
            try:
                pet = Pet.objects.get(id=edit_id)
            except pet.DoesNotExist:
                print "Pet does not exist"
                print edit_id
                return redirect('/pets/')

            pet.name = form.cleaned_data['name']
            pet.save()
            return redirect('/pets/')
        else:
            return render(request, "planner/pets/edit.html", {
                'form': form,
                'edit_id': edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if remove_id:
        pet = Pet.objects.get(id=remove_id)
        pet.delete()
        return redirect('/pets/')
    elif edit_id:
        pet = Pet.objects.get(id=edit_id)
        form = PetForm({
            'name': pet.name,
            'client': pet.client
        })
        form.helper.form_action = '/pets/edit/' + edit_id + '/'
        form.helper.form_id = 'pet-edit-form'
        return render(request, "planner/pets/edit.html", {
            'form': form,
            'edit_id': edit_id,
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
        'form': PetForm
    })


@login_required
def problems(request, edit_id=None, remove_id=None):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = Problem
            try:
                problem = Problem.objects.get(id=edit_id)
            except problem.DoesNotExist:
                return redirect('/problems/')

            problem.name = form.cleaned_data['name']
            problem.code = form.cleaned_data['code']
            problem.color = form.cleaned_data['color']
            problem.save()
            return redirect('/problems/')
        else:
            return render(request, "planner/problems/edit.html", {
                'form': form,
                'edit_id': edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if remove_id:
        problem = Problem.objects.get(id=remove_id)
        problem.delete()
        return redirect('/problems/')
    elif edit_id:
        form = ProblemForm(
            Problem.objects.values().get(id=edit_id)
        )
        form.helper.form_action = '/problems/edit/' + edit_id + '/'
        form.helper.form_id = 'problem-edit-form'
        return render(request, "planner/problems/edit.html", {
            'form': form,
            'edit_id': edit_id,
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
        'form': ProblemForm
    })


@login_required
def visits(request, edit_id=None, remove_id=None):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = Visit
            try:
                visit = Visit.objects.get(id=form.cleaned_data['id'])
            except visit.DoesNotExist:
                return redirect('/visits/')
            visit.from_date = form.cleaned_data['from_date']
            visit.to_date = form.cleaned_data['to_date']
            visit.client = form.cleaned_data['client']
            visit.pet = form.cleaned_data['pet']
            visit.problem = form.cleaned_data['problem']
            visit.description = form.cleaned_data['description']
            visit.appointment_by = User.objects.get(
                id=form.cleaned_data['appointment_by'].id
            )
            visit.appointment_to = User.objects.get(
                id=form.cleaned_data['appointment_to'].id
            )
            visit.save()
            return redirect('/visits/')
        else:
            return render(request, "planner/visits/edit.html", {
                'form': form,
                'edit_id': edit_id,
                'is_register': request.user.groups.filter(name='Registers'),
            })

    if remove_id:
        visit = Visit.objects.get(id=remove_id)
        visit.delete()
        return redirect('/visits/')
    elif edit_id:
        visit = Visit.objects.get(id=edit_id)
        form = VisitForm(initial={
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
        form.helper.form_action = '/visits/edit/' + edit_id + '/'
        form.helper.form_id = 'visit-edit-form'
        return render(request, "planner/visits/edit.html", {
            'form': form,
            'edit_id': edit_id,
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
        'form': VisitForm(initial={
            'appointment_by': Profile.objects.get(
                user__username=request.user
            ).id
        })
    })
