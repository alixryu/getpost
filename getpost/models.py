""":mod:`getpost.models` --- model module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy import String, Boolean, Binary
from sqlalchemy.orm import relationship

from bcrypt import hashpw, gensalt

from .orm import Base

from flask import session as user_session


class Package(Base):
    __tablename__ = 'package'

    id = Column(Integer, primary_key=True)
    sender_name = Column(String)
    student_id = Column(Integer, ForeignKey('student.id'))
    arrival_date = Column(DateTime)
    pickup_date = Column(DateTime)
    received_by = Column(Integer, ForeignKey('employee.id'))
    status = Column(
        Enum('picked_up', 'not_picked_up', name='package_status_type')
    )

    student = relationship(
        'Student',
        lazy='joined'
        )
    employee = relationship(
        'Employee',
        lazy='joined'
        )
    notifications = relationship('Notification')


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    email_address = Column(String)
    send_date = Column(DateTime)
    send_count = Column(Integer)

    package = relationship('Package')


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, unique=True)
    password = Column(Binary)
    verified = Column(Boolean)
    role = Column(
        Enum('student', 'employee', 'administrator', name='account_type')
    )

    student = relationship('Student', uselist=False)
    employee = relationship('Employee', uselist=False)
    administrator = relationship('Administrator', uselist=False)

    login_attributes = {'id', 'role', 'email_address'}

    def set_password(self, password):
        self.password = hashpw(bytes(password, 'ASCII'), gensalt())

    def check_password(self, password):
        return self.password == hashpw(bytes(password, 'ASCII'), self.password)

    def get_person(self):
        if self.role == 'student':
            return self.student
        elif self.role == 'employee':
            return self.employee
        elif self.role == 'administrator':
            return self.administrator
        else:
            return None

    def log_in(self):
        user_session.update(self.as_dict(Account.login_attributes))
        person = self.get_person()
        if person:
            person.log_in()

    def log_out(self):
        for attribute in Account.login_attributes:
            user_session.pop(attribute, None)
        person = self.get_person()
        if person:
            person.log_out()


class Administrator(Base):
    __tablename__ = 'administrator'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account')

    login_attributes = {'first_name', 'last_name'}

    def log_in(self):
        user_session.update(self.as_dict(Administrator.login_attributes))

    def log_out(self):
        for attribute in Administrator.login_attributes:
            user_session.pop(attribute, None)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account')
    packages = relationship(
        'Package',
        lazy='joined'
        )

    login_attributes = {'first_name', 'last_name'}

    def log_in(self):
        user_session.update(self.as_dict(Employee.login_attributes))

    def log_out(self):
        for attribute in Employee.login_attributes:
            user_session.pop(attribute, None)


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    alternative_name = Column(String)
    ocmr = Column(String, unique=True)
    t_number = Column(String)

    account = relationship('Account')
    packages = relationship(
        'Package',
        lazy='joined'
        )

    login_attributes = {
        'first_name', 'last_name', 'alternative_name', 'ocmr', 't_number'
    }

    def log_in(self):
        user_session.update(self.as_dict(Student.login_attributes))

    def log_out(self):
        for attribute in Student.login_attributes:
            user_session.pop(attribute, None)
