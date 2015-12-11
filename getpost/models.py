""":mod:`getpost.models` --- model module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Boolean, Binary

from bcrypt import hashpw

from .orm import Base


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
    role = Column(Enum('student', 'employee', 'administrator', name='account_type'))
    verified = Column(Boolean)


class Administrator(Base):
    __tablename__ = 'administrator'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, ForeignKey('account.id'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    alternative_name = Column(String)
    ocmr = Column(String)
    t_number = Column(Integer)
