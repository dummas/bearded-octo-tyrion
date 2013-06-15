from django.db import models
from django.contrib.auth.management import create_superuser  # Superuser manager
from django.db.models import signals  # Signal handling
from django.contrib.auth import models as auth_models    # Authentication
from django.contrib.auth.models import User
from accounts.models import Profile
from datetime import timedelta
from django.utils import timezone
from datetime import datetime

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)


class ScheduleManager(models.Manager):
    """
    Custom Schedule manager
    """

    def works_on_week(self, date=None):
        """
        Method returns all the doctors, which works on that day
        """
        pass

    def works_on_date(self, date=None):
        """
        Method returns all the doctors, which works today
        """
        if date is None:
            date = timezone.now()

        today_midnight = date
        tomorow_midnight = date
        today_midnight = today_midnight.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        tomorow_midnight = tomorow_midnight.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0)
        schedule = Schedule.objects.filter(
            start__gte=today_midnight,
            start__lte=tomorow_midnight
        ).values(
            'profile__user__username',
            'profile_id',
            'start',
            'end'
        )

        return schedule


class Schedule(models.Model):
    """
    Schedule of the doctor personal

    Manage the working hours of every doctor:
    * user -- doctor
    * start -- start datetime
    * end -- end datetime
    """
    profile = models.ForeignKey(Profile)
    start = models.DateTimeField()
    end = models.DateTimeField()

    objects = ScheduleManager()

    def __unicode__(self):
        return str(self.profile)

    def edit_url(self):
        return "/schedules/edit/" + str(self.id)

    def detele_url(self):
        return "/schedules/remove/" + str(self.id)


class Problem(models.Model):
    """
    The problems
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    color = models.CharField(max_length=200)

    def edit_url(self):
        return "/problems/edit/" + str(self.id)

    def delete_url(self):
        return "/problems/remove/" + str(self.id)

    def __unicode__(self):
        return str(self.code)


class ClientManager(models.Manager):
    """
    Client Manager
    """
    def find_or_create(self, full_name=None):
        """
        Searching for the client by full_name

        full_name consists:
        - first_name
        - last_name
        """
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]

        client = Client
        try:
            client = Client.objects.get(
                first_name=first_name,
                last_name=last_name
            )
        except client.DoesNotExist:
            client = Client(
                first_name=first_name,
                last_name=last_name
            )
            client.save()

        return client


class Client(models.Model):
    """
    The clients
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)

    objects = ClientManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def edit_url(self):
        return '/clients/edit/' + str(self.id)

    def delete_url(self):
        return '/clients/remove/' + str(self.id)


class PetManager(models.Manager):
    """
    Pet Manager
    """
    def find_or_create(self, name=None, client=None):
        """
        Finding the pet

        - name -- name of the pet
        - client -- client of the pet
        """
        pet = Pet
        try:
            pet = Pet.objects.get(
                name=name,
                client=client
            )
        except pet.DoesNotExist:
            pet = Pet(
                name=name,
                client=client
            )
            pet.save()

        return pet


class Pet(models.Model):
    """
    The Pets
    """
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=200)

    objects = PetManager()

    def __unicode__(self):
        return self.name

    def edit_url(self):
        return "/pets/edit/" + str(self.id)

    def delete_url(self):
        return "/pets/remove/" + str(self.id)


class VisitManager(models.Manager):
    """
    Visits manager
    """
    def on_that_day(self, timestamp):
        """
        Method returns all the data, which is on that date, ignoring all the
        hours and minutes
        """
        timestamp = int(timestamp)
        datetime_around = datetime.fromtimestamp(timestamp/1000.0)
        today_midnight = datetime_around
        tomorow_midnight = datetime_around
        today_midnight = today_midnight.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        tomorow_midnight = tomorow_midnight.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0)

        visits = Visit.objects.filter(
            from_date__gte=today_midnight,
            from_date__lte=tomorow_midnight
        )
        # ).values(
        #     'description',
        #     'appointment_to',
        #     'appointment_by',
        #     'client',
        #     'pet',
        #     'from_date',
        #     'to_date',
        #     'problem__color',
        #     'problem',
        #     'id'
        # )

        return visits


class Visit(models.Model):
    """
    The meetings
    """
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    problem = models.ForeignKey(Problem)
    description = models.TextField()
    client = models.ForeignKey(Client)
    pet = models.ForeignKey(Pet)
    appointment_to = models.ForeignKey(User, related_name='doctors')
    appointment_by = models.ForeignKey(User, related_name='registers')

    objects = VisitManager()

    def __unicode__(self):
        return str(self.client.first_name)

    def edit_url(self):
        return '/visits/edit/' + str(self.id)

    def remove_url(self):
        return '/visits/remove/' + str(self.id)


def create_testuser(app, created_models, verbosity, **kwargs):
    """
    Create fast user automatically
    """
    try:
        auth_models.User.objects.get(username='mamunt')
    except auth_models.User.DoesNotExist:
        print 'Creating superuser, login: mamunt, password: pHecAS7s'
        assert auth_models.User.objects.create_superuser(
            'mamunt',
            'm.norkin@gmail.com',
            'pHecAS7s'
        )
    else:
        print 'Test user already exists'


signals.post_syncdb.connect(
    create_testuser,
    sender=auth_models,
    dispatch_uid='common.models.create_testuser'
)
