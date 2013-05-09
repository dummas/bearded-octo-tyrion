from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'planner.views.index'),

    # Visits
    url(r'^visits/$', 'planner.views.visits'),
    url(r'^visits/edit/(?P<visit_edit_id>\d+)/', 'planner.views.visits'),
    url(r'^visits/remove/(?P<visit_remove_id>\d+)/', 'planner.views.visits'),

    # Clients
    url(r'^clients/$', 'planner.views.clients'),
    url(r'^clients/edit/(?P<client_edit_id>\d+)/', 'planner.views.clients'),
    url(r'^clients/remove/(?P<client_remove_id>\d+)/', 'planner.views.clients'),

    # Pets
    url(r'^pets/$', 'planner.views.pets'),
    url(r'^pets/edit/(?P<pet_edit_id>\d+)/', 'planner.views.pets'),
    url(r'^pets/remove/(?P<pet_remove_id>\d+)/', 'planner.views.pets'),

    # Doctors
    url(r'^doctors/$', 'planner.views.doctors'),
    url(r'^doctors/edit/(?P<doctor_edit_id>\d+)', 'planner.views.doctors'),
    url(r'^doctors/remove/(?P<doctor_remove_id>\d+)', 'planner.views.doctors'),

    # Problem
    url(r'^problems/$', 'planner.views.problems'),
    url(r'^problems/edit/(?P<problem_edit_id>\d+)/', 'planner.views.problems'),
    url(r'^problems/remove/(?P<problem_remove_id>\d+)/', 'planner.views.problems'),

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
