# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from employee.views import employeeList


urlpatterns = patterns('',
    url(r'^$', 'employee.views.employee_index', name='employee_list'),
    url(r'^login/$', "employee.views.login", name="user-login"),
    url(r'^employee_detail/(?P<emp_no>[0-9]+)/$', 'employee.views.employee_detail', name='employee_detail'),
    url(r'^employee_list/$', employeeList.as_view(), name='dashboard-employee-list'),
)
