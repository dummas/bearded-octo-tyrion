from django import forms
from django.forms.util import ErrorDict
from django.forms.forms import NON_FIELD_ERRORS
from django.forms import ModelForm
from planner.models import Client
from planner.models import Pet
from planner.models import Problem
from planner.models import Visit


class SinginForm(forms.Form):
    """
    The sing in form
    """
    username = forms.CharField(
        max_length=200)
    password = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput
    )
    remember_me = forms.BooleanField(required=False)

    def add_form_error(self, message):
        if not self._errors:
            self._errors = ErrorDict()
        if not NON_FIELD_ERRORS in self._errors:
            self._errors[NON_FIELD_ERRORS] = self.error_class()
        self._errors[NON_FIELD_ERRORS].append(message)


class ClientForm(ModelForm):
    """
    Client add form
    """
    class Meta:
        model = Client


class PetForm(ModelForm):
    """
    Pet form
    """
    class Meta:
        model = Pet
        fields = ('name', 'client')


class ProblemForm(ModelForm):
    """
    Problem fill in form
    """
    class Meta:
        model = Problem


class VisitForm(ModelForm):
    class Meta:
        model = Visit
