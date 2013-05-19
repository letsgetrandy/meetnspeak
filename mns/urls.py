from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to
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

    url(r'(?i)feedback/$', views.feedback, name="feedback"),

    url(r'(?i)about/$', direct_to_template,
        {'template': 'about.html'}, name='about'),

    #landing pages
    url(r'(?i)apps/$', direct_to_template,
        {'template': 'apps.html'}, name='apps'),
    url(r'(?i)apps/iphone/$', direct_to_template,
        {'template': 'apps-iphone.html'}, name='ios-app'),
    url(r'(?i)apps/android/$', direct_to_template,
        {'template': 'apps-android.html'}, name='droid-app'),
    url(r'(?i)apps/firefox-os/$', direct_to_template,
        {'template': 'apps-firefoxos.html'}, name='b2g-app'),

    #redirects
    url(r'(?i)iphone/$', redirect_to, {'url': '/apps/iphone/'}),
    url(r'(?i)droid/$', redirect_to, {'url': '/apps/android/'}),
    url(r'(?i)android/$', redirect_to, {'url': '/apps/android/'}),
    url(r'(?i)firefoxos/$', redirect_to, {'url': '/apps/firefox-os/'}),
    url(r'(?i)firefox-os/$', redirect_to, {'url': '/apps/firefox-os/'}),

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
