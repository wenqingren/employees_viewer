# -*- coding: utf-8 -*-
from datetime import datetime
import re

from django.db.models import Q

from employee.models import Employee


def get_employee_list(employee=None, sort='emp_no', direction=None, query=None, start=None, end=None):
    employees = Employee.objects.filter(emp_no__in=employee.get_employee_list())

    if query and len(query) > 2:
        if re.match('^\d+$', query):
            employees = employees.filter(emp_no__startswith=query)
        else:
            employees = employees.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(gender=query))

    if sort:
        if direction == 'desc':
            sort = '-' + sort
        employees = employees.order_by(sort)
    data = []
    totalRows = len(employees)
    employees = employees[start:end]
    for employee in employees:
        data.append((
            employee.emp_no,
            employee.first_name,
            employee.last_name,
            employee.gender,
            employee.get_title(),
            datetime.strftime(employee.hire_date, '%d/%m/%Y'),
        ))

    return (data, totalRows)
