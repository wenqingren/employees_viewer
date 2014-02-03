# -*- coding: utf-8 -*-
"""
Unit Test to employee application
"""
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from employee.models import Employee, Department


class employeeTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='1234')
        self.employee1 = Employee.objects.create(user=self.user1, emp_no=123, birth_date=datetime.strptime('1980-01-01', '%Y-%m-%d'), first_name=u'First1', last_name=u'Last1', gender=u'M', hire_date=datetime.strptime('2013-01-01', '%Y-%m-%d'))
        self.user2 = User.objects.create_user(username='user2', password='1234')
        self.employee2 = Employee.objects.create(user=self.user2, emp_no=124, birth_date=datetime.strptime('1980-01-01', '%Y-%m-%d'), first_name=u'First2', last_name=u'Last2', gender=u'F', hire_date=datetime.strptime('2013-01-01', '%Y-%m-%d'))

        self.department = Department.objects.create(dept_no=1, dept_name=u'Dept1')
        self.employee1.departemp_set.create(department=self.department, from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))
        self.employee1.departmanager_set.create(department=self.department, from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))
        self.employee1.salary_set.create(salary=10000, from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))
        self.employee1.title_set.create(title=u'Manager', from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))
        self.employee2.departemp_set.create(department=self.department, from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))
        self.employee2.salary_set.create(salary=6000, from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))
        self.employee2.title_set.create(title=u'Admin', from_date=datetime.strptime('2010-01-01', '%Y-%m-%d'), to_date=datetime.strptime('2015-01-01', '%Y-%m-%d'))

    def test_employee(self):
        # make sure the methods of Employee model are correct
        self.assertEquals(self.employee1.get_full_name(), u'First1 Last1')
        self.assertTrue(self.employee1.is_manager())
        self.assertFalse(self.employee2.is_manager())
        self.assertEquals(len(self.employee1.get_employee_list()), 2)
        self.assertEquals(len(self.employee2.get_employee_list()), 0)
        self.assertEqual(self.employee1.get_title(), u'Manager')
        self.assertEqual(self.employee1.get_department(), u'Dept1')
        self.assertEqual(self.employee1.get_salary(), 10000)
