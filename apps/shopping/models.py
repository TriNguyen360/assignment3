"""
This file defines the database models.
"""

import datetime
from pydal.validators import IS_NOT_EMPTY
from .common import db, Field, auth  # Import necessary objects from common.py

# Define utility functions
def get_time():
    return datetime.datetime.utcnow()

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

# Define the database table for the shopping list
db.define_table(
    'shopping_list',
    Field('item_name', 'string', requires=IS_NOT_EMPTY()),
    Field('is_purchased', 'boolean', default=False),
    Field('user_email', 'string', default=get_user_email),
    Field('added_on', 'datetime', default=get_time),
    Field('checked_on', 'datetime', default=None),
)

# Commit the changes to the database
db.commit()
