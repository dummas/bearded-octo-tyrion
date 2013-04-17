from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print 'Creating groups'
        # Create Registers group
        registers_group = Group.objects.create(name='Register')
        registers_group.permissions.add(
            Permission.objects.get(codename='add_visit'),  # Visits
            Permission.objects.get(codename='change_visit'),
            Permission.objects.get(codename='delete_visit'),
            Permission.objects.get(codename='add_client'),  # Clients
            Permission.objects.get(codename='change_client'),
            Permission.objects.get(codename='add_problem'),  # Problems
            Permission.objects.get(codename='change_problem'),
            Permission.objects.get(codename='add_doctorworking'),  # DW
            Permission.objects.get(codename='change_doctorworking')
        )
        # Create Doctors group
        doctors_group = Group.objects.create(name='Doctor')
        print 'Creating users'
        foo1 = User.objects.create_user(
            'foo1',
            'foo1@gmail.com',
            'brokenwing')
        foo1.groups.add(registers_group)
        foo1.is_staff = True
        foo1.save()
        bar1 = User.objects.create_user(
            'bar1',
            'bar1@gmail.com',
            'brokenwing')
        bar1.groups.add(doctors_group)
        bar1.is_staff = False
