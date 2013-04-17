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


class DoctorForm(forms.Form):
    """
    Entering new doctor form
    """
    name = forms.CharField(
        max_length=200)
    username = forms.CharField(
        max_length=200,
        required=True)
    password = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput)

    def save(self):
        """
        Saving the doctor

        Must include the management of user
        """
        # data = self.cleaned_data


class DoctorsWorking(forms.Form):
    """
    Entering new doctors appointment
    """
    # doctor = forms
