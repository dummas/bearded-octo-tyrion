from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Settings
from django.contrib.auth.management import create_superuser  # Superuser manager
from django.db.models import signals  # Signal handling
from django.contrib.auth import models as auth_models    # Authentication
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)


class DoctorWorking(models.Model):
    """
    The working doctors administration
    """
    doctor = models.ForeignKey(User)  # Think about this place
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()


class Color(models.Model):
    """
    The colors management
    """
    color_code = models.CharField(max_length=12)

    def __unicode__(self):
        return str(self.color_code)


class Problem(models.Model):
    """
    The problems
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    color = models.ForeignKey(Color)

    def __unicode__(self):
        return str(self.code)


class Client(models.Model):
    """
    The clients
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)


class Visit(models.Model):
    """
    The meetings
    """
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    pet_name = models.CharField(max_length=200)
    problem = models.ForeignKey(Problem)
    description = models.TextField()


def create_testuser(app, created_models, verbosity, **kwargs):
    """
    Create fast user automatically
    """
    if not settings.DEBUG:
        return
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
