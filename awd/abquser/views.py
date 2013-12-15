from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import threading

from abquser.models import AbqUser
from abquser.forms import RegistrationForm

    
def UserRegistration(request):
    
    # if the user is already authenticated,
    # redirect them to his/her profile
    if request.user.is_authenticated():
        return HttpResponseRedirect('/console/')
    # if user is registering
    if request.method == 'POST':
        # get the form they just posted
        form =RegistrationForm(request.POST)
        # if the form is valid
        if form.is_valid():
            # get their username and password
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            # create the user
            user = User.objects.create_user(username=username,
                                            password=password)
            # set first name, last name and email address
            user.email      = username
            user.first_name = form.cleaned_data['firstname']
            user.last_name  = form.cleaned_data['lastname']
            # set the user as inactive and wait for confirmation
            user.is_active  = False
            # save the user into data-base
            user.save()
            # now create an abaqual user
            abquser = AbqUser(user=user)
            # save abaqual user into database
            abquser.save()
            # email the user activation link
            registration_confirmation_email(request,abquser)
            # and redirect them to thank you page
            return render_to_response('registration_thankyou.html')
        # if the form is not valid show then the form again
        else:
            return render_to_response(
                'registration.html', {'form':form}, 
                context_instance=RequestContext(request))
   
    # otherwise show the user an empty form
    else:
        form = RegistrationForm()
        return render_to_response(
            'registration.html', {'form':form}, 
            context_instance=RequestContext(request))


def registration_confirmation_email(request,abquser):
    """ Send a registration confirmation.

    This email contains a link to activate their registation
    """
    domain_name = request.build_absolute_uri('/')
    email_subject = 'Your new Abaqual account confirmation'
    email_body = 'Hello %s, and thanks for signing up '\
        'for an Abaqual account!\n\n ' \
        'To activate your account, click this '\
        'link within 7 days:\n\n' \
        '%sregistration-confirmation/%s' \
        %(abquser.user.first_name, domain_name, 
          abquser.activation_key)
    thread = threading.Thread(target=send_mail,
                              args=(email_subject,email_body,
                                    settings.EMAIL_HOST_USER,
                                    [abquser.user.email]))
    thread.start()
