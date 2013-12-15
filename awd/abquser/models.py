from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from common.funcs import get_sha1
import datetime

class AbqUser(models.Model):
    """ Abaqual users class 

    Abaqual user is a Django User with the following features:
    - activation key and its expiration date.
    - tokens to purchase compute hours and tools.
    """
    user           = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expiration = models.DateTimeField()
    coins          = models.FloatField(default=0.0)


    def __unicode__(self):
        return self.user.username


    def __init__(self,*arguments,**kwargs):
        # initialize the base class
        super(AbqUser, self).__init__(*arguments,**kwargs)
        self.activation_key = get_sha1(self.user.username)
        self.key_expiration = timezone.now() + datetime.timedelta(days=7)
                

    class Meta:
        verbose_name = 'Abaqual user'
        permissions = (
            ('launch_workspace', 'Can launch a workspace'),
            ('launch_company', 'Can create a company'),
            ('post_project', 'Can post a project'),
            ('post_software', 'Can post a software'),
            )
