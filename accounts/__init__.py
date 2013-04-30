from django.db.models.signals import post_syncdb
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import accounts.models


def create_user_groups(sender, **kwargs):
    # Create Registers group
    defined_group = Group(name='Registers')
    defined_group.save()
    # Create Doctors group
    defined_group = Group(name='Doctors')
    defined_group.save()


def create_test_users(sender, **kwargs):
    # Create three doctors
    foo1_doctor = User.objects.create_user(
        'foo1',
        'foo1@bar1.com',
        'bar1'
    )
    foo2_doctor = User.objects.create_user(
        'foo2',
        'foo2@bar1.com',
        'bar2'
    )
    foo3_doctor = User.objects.create_user(
        'foo3',
        'foo3@bar1.com',
        'bar3'
    )
    foo1_doctor.save()
    foo2_doctor.save()
    foo3_doctor.save()

    # Create three test registers
    bar1_register = User.objects.create_user(
        'bar1',
        'bar1@foo1.com',
        'foo1'
    )
    bar2_register = User.objects.create_user(
        'bar2',
        'bar2@foo1.com',
        'foo2'
    )
    bar3_register = User.objects.create_user(
        'bar3',
        'bar3@foo1.com',
        'foo3'
    )
    bar1_register.save()
    bar2_register.save()
    bar3_register.save()

    # Assign users to groups
    doctors_group = Group.objects.get(name='Doctors')
    doctors_group.user_set.add(foo1_doctor)
    doctors_group.user_set.add(foo2_doctor)
    doctors_group.user_set.add(foo3_doctor)
    register_group = Group.objects.get(name='Registers')
    register_group.user_set.add(bar1_register)
    register_group.user_set.add(bar2_register)
    register_group.user_set.add(bar3_register)

post_syncdb.connect(create_user_groups, sender=accounts.models)
post_syncdb.connect(create_test_users, sender=accounts.models)
