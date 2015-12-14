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
    admin = relationship('Administrator', uselist=False, back_populates='account')

    def set_password(self, password):
        self.password = hashpw(bytes(password, 'ASCII'), gensalt())

    def check_password(self, password):
        return self.password == hashpw(bytes(password, 'ASCII'), self.password)

    def log_in(self):
        session['logged_in'] = True
        session['id'] = self.id
        session['role'] = self.role
        session['email_address'] = self.email_address

    def log_out(self):



class Administrator(Base):
    __tablename__ = 'administrator'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account', back_populates='admin')


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    account = relationship('Account', back_populates='employee')


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    alternative_name = Column(String)
    ocmr = Column(String)
    t_number = Column(Integer)

    account = relationship('Account', back_populates='student')
