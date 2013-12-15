from django.db import models
from django.contrib.auth.models import User, Group, Permission
from abquser.models import AbqUser

# =============
# create groups
# =============

# professional 
group, created = Group.objects.get_or_create(name='professional')
if created:
    print 'group', group.name, 'created ...'
group.save()
    
# expert
group, created = Group.objects.get_or_create(name='expert')
if created:
    print 'group', group.name, 'created ...'
group.save()


# ==============
# Abaqual users
# ==============

user, created = User.objects.get_or_create(username='jo@jo.com')
if created:
    print 'user', user.username, 'created ...'
user.first_name = 'Jo'
user.last_name = 'Jo'
user.is_active = True
user.set_password('jo')
user.groups = Group.objects.filter(name='professional')
user.user_permissions = Permission.objects.filter(
    codename='post_software')
user.save()
abquser, created = AbqUser.objects.get_or_create(user=user)
if created:
    print 'abaqual user', user.username, 'created ...'
abquser.save()
