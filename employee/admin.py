# -*- coding: utf-8 -*-
from django.contrib import admin

from employee.models import Employee, Department, DepartEmp, DepartManager, Salary, Title


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date' )
    search_fields = ['emp_no', 'first_name', 'last_name']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_no', 'dept_name')
    search_fields = ['dept_no', 'dept_name']


class DepartEmpAdmin(admin.ModelAdmin):
    list_display = ('employee', 'department', 'from_date', 'to_date')
    search_fields = ['employee', 'department']


class DepartManagerAdmin(admin.ModelAdmin):
    list_display = ('department', 'employee', 'from_date', 'to_date')
    search_fields = ['department', 'employee']


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'from_date', 'to_date')
    search_fields = ['employee', 'salary']


class TitleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'from_date', 'to_date')
    search_fields = ['employee', 'title']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartEmp, DepartEmpAdmin)
admin.site.register(DepartManager, DepartManagerAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Title, TitleAdmin)
