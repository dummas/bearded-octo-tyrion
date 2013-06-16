from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'planner.views.index'),
    url(r'^view/(?P<view>[\w-]+)/$', 'planner.views.index'),
    url(r'^view/(?P<view>[\w-]+)/day/(?P<days>[\w-]+)/$', 'planner.views.index'),
    url(r'^view/(?P<view>[\w-]+)/week/(?P<weeks>[\w-]+)/$', 'planner.views.index'),
    url(r'^view/(?P<view>[\w-]+)/month/(?P<months>[\w-]+)/$', 'planner.views.index'),

    # Visits
    url(r'^visits/$', 'planner.views.visits'),
    url(r'^visits/edit/(?P<edit_id>\d+)/', 'planner.views.visits'),
    url(r'^visits/remove/(?P<remove_id>\d+)/', 'planner.views.visits'),

    # Clients
    url(r'^clients/$', 'planner.views.clients'),
    url(r'^clients/edit/(?P<edit_id>\d+)/', 'planner.views.clients'),
    url(r'^clients/remove/(?P<remove_id>\d+)/', 'planner.views.clients'),

    # Pets
    url(r'^pets/$', 'planner.views.pets'),
    url(r'^pets/edit/(?P<edit_id>\d+)/', 'planner.views.pets'),
    url(r'^pets/remove/(?P<remove_id>\d+)/', 'planner.views.pets'),

    # Doctors
    url(r'^profiles/$', 'accounts.views.profiles'),
    url(r'^profiles/edit/(?P<edit_id>\d+)', 'accounts.views.profiles'),
    url(r'^profiles/remove/(?P<remove_id>\d+)', 'accounts.views.profiles'),

    # Schedules
    url(r'^schedules/$', 'planner.views.schedules'),
    url(r'^schedules/edit/(?P<edit_id>\d+)', 'planner.views.schedules'),
    url(r'^schedules/remove/(?P<remove_id>\d+)', 'planner.views.schedules'),

    # Problem
    url(r'^problems/$', 'planner.views.problems'),
    url(r'^problems/edit/(?P<edit_id>\d+)/', 'planner.views.problems'),
    url(r'^problems/remove/(?P<remove_id>\d+)/', 'planner.views.problems'),

    # Accounts
    url(r'^accounts/login/$', 'accounts.views.account_login'),
    url(r'^accounts/logout/$', 'accounts.views.account_logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # API
    url(r'^api/', include('api.urls'))
)

urlpatterns += staticfiles_urlpatterns()
