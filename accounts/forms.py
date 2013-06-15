from django import forms
from django.forms.widgets import PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Div
from crispy_forms.bootstrap import AppendedText
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit
from crispy_forms.layout import Button


class ProfileForm(forms.Form):
    """
    The doctor form
    """
    username = forms.CharField(
        max_length=200,
        help_text='Doctor username'
    )
    email = forms.CharField(
        max_length=200,
        help_text='doctor.username@email.com'
    )
    password1 = forms.CharField(
        widget=PasswordInput,
        label='Password',
        help_text='First password'
    )
    password2 = forms.CharField(
        widget=PasswordInput,
        label='Password repeat',
        help_text='Repeat the password to be sure'
    )

    def clean_passwords(self):
        """
        Password checking
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1:
            raise forms.ValidationError('No password input')
        if not password2:
            raise forms.ValidationError('No password repeat input')
        if password1 != password2:
            raise forms.ValidationError('Passwords not match')
        return password2

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/api/profiles/'
        self.helper.form_id = 'doctor-add-form'
        self.helper.layout = Layout(
            Div(
                Div(
                    'username',
                    css_class='span6'
                ),
                Div(
                    AppendedText(
                        'email',
                        '<i class="icon-envelope"></i>'
                    ),
                    css_class='span6',
                ),
                css_class='row-fluid'
            ),
            Div(
                Div(
                    'password1',
                    css_class='span6'
                ),
                Div(
                    'password2',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel', css_class='btn', data_dismiss='model')
            )
        )
        super(ProfileForm, self).__init__(*args, **kwargs)
