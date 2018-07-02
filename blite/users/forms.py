from django import forms
from . import models
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserUpdateForm(forms.ModelForm): # omit username - username cannot be changed

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    HTTP_method = forms.CharField(initial="PUT", widget=forms.HiddenInput())


class UserDeleteForm(forms.Form): # this one does not inherit from modelForm, just a basic form
    
    HTTP_method = forms.CharField(initial="DELETE", widget=forms.HiddenInput())
    CONFIRMATION_CHOICES = (('NO', 'NO'), ('YES', 'YES'))
    confirmation = forms.ChoiceField(choices = CONFIRMATION_CHOICES,
                                initial='NO',
                                widget=forms.Select(),
                                required=True)

