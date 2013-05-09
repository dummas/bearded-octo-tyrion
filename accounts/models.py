from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return str(self.user.username)

    def get_username(self):
        return str(self.user.username)

    def edit_url(self):
        return "/accounts/edit/" + str(self.id)

    def remove_url(self):
        return "/accounts/remove/" + str(self.id)


def create_user_profile(
    sender,
    instance,
    created,
    **kwargs
):
    if created:
        profile, created = Profile.objects.get_or_create(
            user=instance
        )
post_save.connect(create_user_profile, sender=User)
