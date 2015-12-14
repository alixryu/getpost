""":mod:`getpost.models` --- model module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy import String, Boolean, Binary
from sqlalchemy.orm import relationship

from bcrypt import hashpw, gensalt

from .orm import Base

from flask import session


class Package(Base):
    __tablename__ = 'package'

    id = Column(Integer, primary_key=True)
    student_id = Column(String)
    arrival_date = Column(DateTime)
    pickup_date = Column(DateTime)
    received_by = Column(String)
    status = Column(
        Enum('picked_up', 'not_picked_up', name='package_status_type')
    )


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    email_address = Column(String)
    send_date = Column(DateTime)
    send_count = Column(DateTime)


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email_address = Column(String)
    password = Column(Binary)
    verified = Column(Boolean)
    role = Column(
        Enum('student', 'employee', 'administrator', name='account_type')
    )

    student = relationship('Student', uselist=False, back_populates='account')
    employee = relationship('Employee', uselist=False, back_populates='account')
    administrator = relationship('Administrator', uselist=False, back_populates='account')

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
        session['logged_in'] = True
        session['id'] = self.id
        session['role'] = self.role
        session['email_address'] = self.email_address
        person = self.get_person()
        if person:
            person.log_in()

    def log_out(self):
        for attribute in ('logged_in', 'id', 'role', 'email_address'):
            session.pop(attribute, None)
        person = self.get_person()
        if person:
            person.log_out()


class Administrator(Base):
    __tablename__ = 'administrator'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account', back_populates='administrator')

    def log_in(self):
        session['first_name'] = self.first_name
        session['last_name'] = self.last_name

    def log_out(self):
        for attribute in ('first_name', 'last_name'):
            session.pop(attribute, None)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account', back_populates='employee')

    def log_in(self):
        session['first_name'] = self.first_name
        session['last_name'] = self.last_name

    def log_out(self):
        for attribute in ('first_name', 'last_name'):
            session.pop(attribute, None)


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    alternative_name = Column(String)
    ocmr = Column(String)
    t_number = Column(Integer)

    account = relationship('Account', back_populates='student')

    def log_in(self):
        session['first_name'] = self.first_name
        session['last_name'] = self.last_name
        session['alternative_name'] = self.alternative_name
        session['ocmr'] = self.ocmr
        session['tnum'] = self.t_number

    def log_out(self):
        for attribute in ('first_name', 'last_name', 'alternative_name', 'ocmr', 'tnum'):
            session.pop(attribute, None)
