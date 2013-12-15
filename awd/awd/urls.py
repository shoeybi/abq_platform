from django.conf.urls import patterns, include, url
# enable admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(

    # no generic view pattern
    '',
    
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # registration
    url(r'^register/$','abquser.views.UserRegistration'),

)
