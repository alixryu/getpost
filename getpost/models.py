""":mod:`getpost.models` --- model module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy import String, Boolean, Binary
from sqlalchemy.orm import relationship

from bcrypt import hashpw, gensalt

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
    role = Column(
        Enum('student', 'employee', 'administrator', name='account_type')
    )
    verified = Column(Boolean)

<<<<<<< HEAD
    def set_password(self, password):
        self.password = hashpw(bytes(password, 'ASCII'), gensalt())

    def check_password(self, password):
        return self.password == hashpw(bytes(password, 'ASCII'), self.password)
=======
    student = relationship('Student', uselist=False, back_populates='account')
>>>>>>> 4013dc33fd09f4c3a2da41973954677bc0971f2c


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

    account = relationship('Account', back_populates='student')
