from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mns.views.index', name='index'),
    url(r'(?i)login/$', 'mns.views.login', name='login'),
    url(r'(?i)signup/$', 'mns.views.signup', name='signup'),
    url(r'(?i)search/$', 'mns.views.search', name='search'),
    url(r'(?i)user/$', 'mns.views.profile', name='profile'),
    url(r'(?i)user/contacts/$', 'mns.views.contacts', name='contacts'),
    url(r'(?i)user/settings/$', 'mns.views.settings', name='settings'),
    url(r'(?i)user/(?P<userid>\d+)/$', 'mns.views.user', name='user'),
    url(r'(?i)user/(?P<userid>\d+)/messages/$', 'mns.views.messages',
        name='messages'),

    # Examples:
    # url(r'^$', 'mns.views.home', name='home'),
    # url(r'^mns/', include('mns.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
