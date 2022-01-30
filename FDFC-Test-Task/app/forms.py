import datetime
import re

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from app.models import CustomUser

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, help_text='Enter a username (make sure that it is unique)', widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input'}), help_text='Enter your password again')
    email = forms.EmailField(help_text='Enter your email address', widget=forms.TextInput(attrs={'class' : 'input'}))

    def clean_id_num(self):
        cleaned_data = super().clean()

        data = self.cleaned_data.get('password')
        data2 = self.cleaned_data.get('confirm_password')

        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')         

        rules = [lambda data: any(x.isupper() for x in data), # must have at least one uppercase
        lambda data: any(x.islower() for x in data),  # must have at least one lowercase
        lambda data: any(x.isdigit() for x in data),  # must have at least one digit
        lambda data: len(data) >= 8,                  # must be at least 8 characters
        lambda data: string_check.search(data) != None,  # must have at least one special character
        # lambda data: data == data2,  # must be equal to the confirm password
        ]        
        
        if not all(rule(data) for rule in rules):
            raise ValidationError(_('Password must have at least one uppercase, one lowercase, and a special character with a minimum of 8 characters.'))            
        elif data != data2:
            raise ValidationError(_('Password and confirm password must match.'))
        else:
            return data

    class Meta():
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), help_text="Enter username", max_length=30, widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class' : 'input'}))

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
    
    def confirm_login_allowed(self, user):
        if not user:
            raise forms.ValidationError(_('User does not exist'))
        elif not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')