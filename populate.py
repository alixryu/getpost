#!/usr/bin/env python3

""":script:`getpost.database.populate` --- script for populating database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import csv

from sqlalchemy import MetaData

from getpost.models import Account, Student
from getpost.orm import engine, Session


CSV_FILE = 'OCMRs.csv'


def populate_account(csv_dictreader, session):
    for row in csv_dictreader:
        account = Account(
            email_address=row['email_id']+'@oberlin.edu',
            password=row['email_id'],
            role='student'
        )
        session.add(account)


def populate_student(csv_dictreader, session):
    for row in csv_dictreader:
        s_account = session.query(Account).filter_by(
            email_address=row['email_id']+'@oberlin.edu'
        ).one()
        student = Student(
            id=s_account.id,
            first_name=row['first_name'],
            last_name=row['last_name'],
            alternative_name='',
            ocmr=row['ocmr'],
            t_number=0
        )
        session.add(student)

if __name__ == '__main__':

    metadata = MetaData(bind=engine)

    with open(CSV_FILE) as f:
        # assume first line is header
        cf = csv.DictReader(f, delimiter=',')

        session = Session()
        try:
            populate_account(cf, session)
            session.commit()
            # reset iterator
            f.seek(0)
            # assume first line is header
            f.readline()
            populate_student(cf, session)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
