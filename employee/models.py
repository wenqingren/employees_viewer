# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    dept_no = models.CharField(max_length=4, primary_key=True)
    dept_name = models.CharField(max_length=40)

    class meta:
        db_table = 'departments'

    def __unicode__(self):
        return u'No %s: %s' % (self.dept_no, self.dept_name)


class Employee(models.Model):
    GENDER_CHOICE = (
        ('M', u'Male'),
        ('F', u'Female'),
    )

    user = models.ForeignKey(User, unique=True)
    emp_no = models.PositiveIntegerField(max_length=11, primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    hire_date = models.DateField()

    class meta:
        db_table = 'employees'

    def __unicode__(self):
        return u'Employee %s: %s %s, Gender: %s' % (str(self.emp_no), self.first_name, self.last_name, self.gender)

    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def is_manager(self):
        return self.departmanager_set.filter(from_date__lte=datetime.now(), to_date__gte=datetime.now()).count() > 0

    def get_employee_list(self):
        if not self.is_manager:
            return []

        employees = []
        for department in self.departmanager_set.filter(from_date__lte=datetime.now(), to_date__gte=datetime.now()):
            for employee in department.department.departemp_set.filter(from_date__lte=datetime.now(), to_date__gte=datetime.now()):
                employees.append(employee.employee.emp_no)
        return list(set(employees))

    def get_title(self):
        return  ', '.join(x.title for x in self.title_set.filter(from_date__lte=datetime.now(), to_date__gte=datetime.now()))

    def get_department(self):
        return  ', '.join(x.department.dept_name for x in self.departemp_set.filter(from_date__lte=datetime.now(), to_date__gte=datetime.now()))

    def get_salary(self):
        try:
            return self.salary_set.filter(from_date__lte=datetime.now(), to_date__gte=datetime.now())[0].salary
        except IndexError:
            return 0


class DepartEmp(models.Model):
    employee = models.ForeignKey(Employee)
    department = models.ForeignKey(Department)
    from_date = models.DateField()
    to_date = models.DateField()

    class meta:
        db_table = 'dept_emp'
        unique_together = ('employee', 'department')

    def __unicode__(self):
        return '%s in Department %s from %s to %s' % (self.employee.get_full_name(), self.department.dept_name, datetime.strftime(self.from_date, '%Y-%m-%d'), datetime.strftime(self.to_date, '%Y-%m-%d'))


class DepartManager(models.Model):
    department = models.ForeignKey(Department)
    employee = models.ForeignKey(Employee)
    from_date = models.DateField()
    to_date = models.DateField()

    class meta:
        db_table = 'dept_manager'
        unique_together = ('department', 'employee')

    def __unicode__(self):
        return 'Department %s Manager: %s from %s to %s' % (self.department.dept_name, self.employee.get_full_name(), datetime.strftime(self.from_date, '%Y-%m-%d'), datetime.strftime(self.to_date, '%Y-%m-%d'))


class Salary(models.Model):
    employee = models.ForeignKey(Employee)
    salary = models.PositiveIntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    class meta:
        db_table = 'salaries'
        unique_together = ('employee', 'from_date')

    def __unitcode__(self):
        return '%s salary $%s from %s to %s' % (self.employee.get_full_name(), str(self.salary), datetime.strftime(self.from_date, '%Y-%m-%d'), datetime.strftime(self.to_date, '%Y-%m-%d'))


class Title(models.Model):
    employee = models.ForeignKey(Employee)
    title = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()

    class meta:
        db_table = 'titles'
        unique_together = ('employee', 'title', 'from_date')

    def __unitcode__(self):
        return '%s title $%s from %s to %s' % (self.employee.get_full_name(), self.title, datetime.strftime(self.from_date, '%Y-%m-%d'), datetime.strftime(self.to_date, '%Y-%m-%d'))

