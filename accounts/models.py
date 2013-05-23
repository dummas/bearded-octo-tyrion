from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ProfileManager(models.Manager):
    """
    Profile manager
    """
    def are_doctors(self):
        """
        Profile filter, returning doctors only
        """
        return Profile.objects.filter(user__groups__name='Doctors')

    def are_registers(self):
        """
        Profile filter, returning registers only
        """
        return Profile.objects.filter(user__groups__name='Registers')


class Profile(models.Model):
    """
    Profile model
    one field only
    """

    user = models.OneToOneField(User)
    objects = ProfileManager()

    def __unicode__(self):
        """
        Unicode returning the username
        """
        return str(self.user.username)

    def get_username(self):
        """
        Returns username
        """
        return str(self.user.username)

    def edit_url(self):
        """
        Returns the edit anchor
        """
        return "/accounts/edit/" + str(self.id)

    def remove_url(self):
        """
        Returns the remove anchor
        """
        return "/accounts/remove/" + str(self.id)


def create_user_profile(
    sender,
    instance,
    created,
    **kwargs
):
    """
    Creating user profile
    """
    if created:
        profile, created = Profile.objects.get_or_create(
            user=instance
        )
post_save.connect(create_user_profile, sender=User)
