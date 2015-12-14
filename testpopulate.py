#!/usr/bin/env python3

""":script:`getpost.database.populate` --- script for creating dummy student,
employee, and administrator accounts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from sqlalchemy import MetaData

from getpost.models import Account, Student, Employee, Administrator
from getpost.orm import engine, Session


CSV_FILE = 'OCMRs.csv'

def add_account(**kwargs):
    kwargs['verified'] = True
    account = Account(**kwargs)
    account.set_password('password')
    Session.add(account)
    Session.commit()
    return account.id

def add_student(first_name='Test', last_name='Student', alternative_name='Obie', email_address='student@oberlin.edu'):
    id = add_account(email_address=email_address, role='student')
    student = Student(id=id, first_name=first_name, last_name=last_name, ocmr='10000')
    Session.add(student)

def add_employee():
    id = add_account(email_address='employee@oberlin.edu', role='employee')
    employee = Employee(id=id, first_name='Test', last_name='Account')
    Session.add(employee)

def add_admin():
    id = add_account(email_address='admin@oberlin.edu', role='administrator')
    admin = Administrator(id=id, first_name='Test', last_name='Administrator')
    Session.add(admin)


if __name__ == '__main__':

    metadata = MetaData(bind=engine)

    try:
        add_student()
        Session.commit()
        add_employee()
        Session.commit()
        add_admin()
        Session.commit()
    except:
        Session.rollback()
        raise
    finally:
        Session.close()
