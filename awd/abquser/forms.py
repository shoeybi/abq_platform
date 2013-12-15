from django import forms
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.forms.util import ErrorDict, ErrorList
from abquser.models import AbqUser


class RegistrationForm(forms.Form):
    
    # minimum information required for registration
    username  = forms.EmailField(label=(u'Email Address'))
    firstname = forms.CharField(label=(u'First Name'))
    lastname  = forms.CharField(label=(u'Last Name'))
    password  = forms.CharField(
        label=(u'Password'), 
        widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(
        label=(u'Verify Password'), 
        widget=forms.PasswordInput(render_value=False))
    
    
    def clean(self):
        # first we need to get access to the original cleaned_data method
        cleaned_data = super(RegistrationForm,self).clean()
        
        # get the username from the form
        username = cleaned_data.get('username')
        # if there was a validation error then email has not been a valid one
        if username == None:
            if not self._errors:
                self._errors = ErrorDict()
            self._errors['username'] = \
                ErrorList([u' Email address is not valid.'])
        else:
            # otherwise try to find if the username is in the database
            username = username.lower()
            try:
                User.objects.get(username=username)
            # if user does not exist then it is valid
            except User.DoesNotExist:
                pass
            # otherwise raise an error
            else:
                if not self._errors:
                    self._errors = ErrorDict()
                self._errors['username'] = \
                    ErrorList([username+' is already taken.'])

        # get the firstname from the form
        firstname = cleaned_data.get('firstname')
        # if there was a validation error then 
        # firstname has not been a valid one
        if firstname == None:
            if not self._errors:
                self._errors = ErrorDict()
            self._errors['firstname'] = \
                ErrorList([u'First name is not valid.'])

        # get the lastname from the form
        lastname = cleaned_data.get('lastname')
        # if there was a validation error then 
        # lastname has not been a valid one
        if lastname == None:
            if not self._errors:
                self._errors = ErrorDict()
            self._errors['lastname'] = \
                ErrorList([u'Last name is not valid.'])

        # password
        # get the password from the form
        password = cleaned_data.get('password')
        # if there was a validation error then 
        # password has not been a valid one
        if password == None:
            if not self._errors:
                self._errors = ErrorDict()
            self._errors['password'] = \
                ErrorList([u'Password is not valid.'])
            
        # get the password from the form
        password1 = cleaned_data.get('password1')
        # if there was a validation error then 
        # password has not been a valid one
        if password1 == None:
            if not self._errors:
                self._errors = ErrorDict()
            self._errors['password1'] = \
                ErrorList([u'Password is not valid.'])
            
        # check that the two passwords are the same
        if password != password1:
            raise forms.ValidationError("Passwords did not match")

        # return cleaned_data so the methods returns 
        # the full list of cleaned_data
        return self.cleaned_data



