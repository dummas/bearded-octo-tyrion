from django import forms
from django.forms.util import ErrorDict
from django.forms.forms import NON_FIELD_ERRORS


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


class ClientForm(forms.Form):
    """
    Client add form
    """
    first_name = forms.CharField(
        max_length=200
    )
    last_name = forms.CharField(
        max_length=200
    )
    telephone = forms.CharField(
        max_length=200
    )


class DoctorForm(forms.Form):
    """
    Entering new doctor form
    """
    pass


class DoctorWorkingForm(forms.Form):
    """
    Entering new doctors appointment
    """
    pass
