from django.conf.urls import patterns, include, url
from django.conf import settings
from mns import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'(?i)login/$', views.login, name='login'),
    url(r'(?i)logout/$', views.logout, name='logout'),
    url(r'(?i)signup/$', views.signup, name='signup'),
    url(r'(?i)search/$', views.search, name='search'),
    url(r'(?i)search.ajax$', views.search_ajax, name='search-ajax'),
    url(r'(?i)user/$', views.profile, name='profile'),
    url(r'(?i)user/notifications/$', views.notifications, name='notifications'),
    url(r'(?i)user/contacts/$', views.contacts, name='contacts'),
    url(r'(?i)user/settings/$', views.user_settings, name='settings'),
    url(r'(?i)user/(?P<userid>\d+)/$', views.user, name='user'),
    url(r'(?i)user/(?P<userid>\d+)/messages/$', views.messages,
        name='messages'),
    url(r'(?i)user/image-upload/$', views.image, name='image-ajax'),

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
