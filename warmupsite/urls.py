from django.conf.urls import patterns, include, url
from django.views.static import serve
from login.views import login, add, resetFixture, testUnit, initpage
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmupsite.views.home', name='home'),
    # url(r'^warmupsite/', include('warmupsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^users/login$', login),
    url(r'^users/add$', add),
    url(r'^TESTAPI/resetFixture$', resetFixture),
    url(r'^TESTAPI/unitTests$', testUnit),
    url(r'^$', initpage),
    url(r'^(?P<path>.*css)$', 'django.views.static.serve', {'document_root': os.path.abspath('/home/az/cs169/warmupsite/warmupsite/templates')}),
    url(r'^(?P<path>.*js)$', 'django.views.static.serve', {'document_root': os.path.abspath('/home/az/cs169/warmupsite/warmupsite/templates')}),

)
