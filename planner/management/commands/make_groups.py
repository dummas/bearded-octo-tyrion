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
            'bar1')
        foo1.groups.add(doctors_group)
        foo1.is_staff = False
        foo1.save()
        foo2 = User.objects.create_user(
            'foo2',
            'foo1@gmail.com',
            'bar2')
        foo2.groups.add(doctors_group)
        foo2.is_staff = False
        foo2.save()
        foo3 = User.objects.create_user(
            'foo3',
            'foo1@gmail.com',
            'bar3')
        foo3.groups.add(doctors_group)
        foo3.is_staff = False
        foo3.save()

        bar1 = User.objects.create_user(
            'bar1',
            'bar1@gmail.com',
            'brokenwing')
        bar1.groups.add(registers_group)
        bar1.is_staff = True
        bar1.save()
