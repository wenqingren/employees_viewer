# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View

from employee.models import Employee
from employee.utils import get_employee_list


def r(template_name, dictionary, request):
    return render_to_response(template_name,
                              dictionary,
                              context_instance=RequestContext(request))

def login(request, template_name = 'employee/login.html'):
    if request.POST:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        if username is not None and password is not None:
            if request.user.is_authenticated():
                auth.logout(request)

            user = None
            for found_user in Employee.objects.filter(emp_no=password):
                if found_user.first_name + found_user.last_name == username:
                    user = found_user
                    break
            if user is not None and user.is_active:
                auth.login(request, user)

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                nu = request.GET.get('next', '')

                return HttpResponseRedirect(nu)

            return r(template_name, {"error_message": _('Username / Password is wrong'),
                'full_path': request.get_full_path()}, request)
        return r(template_name, {"error_message": _('Please enter your username / password'),
            'full_path': request.get_full_path()}, request)
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('')
        else:
            return r(template_name, {'full_path': request.get_full_path()}, request)


@login_required
def employee_index(request):
    employee = get_object_or_404(Employee, user=request.user)
    if not employee.is_manager():
        return HttpResponseRedirect(reverse('employee_detail', args=[employee.emp_no]))
    t = loader.get_template('employee/index.html')
    context_values = {'employee': employee}
    c = Context(context_values)
    return HttpResponse(t.render(c))


@login_required
def employee_detail(request, emp_no):
    employee = get_object_or_404(Employee, emp_no=int(emp_no))

    t = loader.get_template('employee/employee_details.html')
    c = Context({
        'employee': employee,
        'department': employee.get_department(),
        'title': employee.get_title(),
        'hire_years': round((datetime.now().date() - employee.hire_date).days/365, 2),
        'age_years': round((datetime.now().date() - employee.birth_date).days/365, 2),
        'salary': employee.get_salary()
    })
    return HttpResponse(t.render(c))


class employeeList(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        employee = get_object_or_404(Employee, user=request.user)
        get = request.GET
        data = {
            'aaData': [],
            'iTotalRecords': 0,
            'iTotalDisplayRecords': 0
        }

        start = int(get.get('iDisplayStart', 0))
        limit = int(get.get('iDisplayLength', 10))
        query = get.get('sSearch', None)

        sort = int(get.get('iSortCol_0', 0))
        direction = get.get('sSortDir_0', None)
        columns = ('emp_no', 'first_name', 'last_name', 'gender', 'title', 'hire_date',)
        sort = columns[sort]

        renderRows, totalRows = get_employee_list(employee=employee, sort=sort, direction=direction, query=query, start=start, end=start + limit)
        data['iTotalRecords'] = totalRows
        data['iTotalDisplayRecords'] = data['iTotalRecords']
        for row in renderRows:
            data['aaData'].append(row)

        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
