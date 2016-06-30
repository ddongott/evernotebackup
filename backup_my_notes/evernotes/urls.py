from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="evernote_index"),
    url(r'^auth/$', views.auth,name="evernote_auth"),
    url(r'^callback/$', views.callback, name="evernote_callback"),
    url(r'^savenotes/$', views.savenotes, name="evernote_savenotes"),
    url(r'^reset/$', views.reset, name="evernote_auth_reset"),
]

