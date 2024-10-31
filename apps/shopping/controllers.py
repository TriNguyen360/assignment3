import uuid
from py4web import action, request, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from datetime import datetime
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

def get_time():
    return datetime.utcnow()

@action('index')
@action.uses('index.html', db, session, auth.user)
def index():
    return dict(
        load_data_url=URL('load_data'),
        add_item_url=URL('add_item'),
        mark_purchased_url=URL('mark_purchased'),
        delete_item_url=URL('delete_item'),
    )

@action('load_data', method='GET')
@action.uses(db, auth.user)
def load_data():
    user_email = get_user_email()
    # Order items: unchecked items first, checked items next, sorted by ID descending
    items = db(db.shopping_list.user_email == user_email).select(
        orderby=[db.shopping_list.is_purchased, ~db.shopping_list.id]
    ).as_list()
    return dict(items=items)

@action('add_item', method='POST')
@action.uses(db, auth.user)
def add_item():
    user_email = get_user_email()
    item_name = request.json.get('item_name')
    if not item_name:
        return dict(error="Item name is required.")
    
    # Insert new item with the user_email to associate it with the current user
    db.shopping_list.insert(
        user_email=user_email,
        item_name=item_name,
        is_purchased=False,
        added_on=get_time()  # Added timestamp for the new item
    )
    return dict(message="Item added successfully.")

@action('mark_purchased', method='POST')
@action.uses(db, auth.user)
def mark_purchased():
    user_email = get_user_email()
    item_id = request.json.get('item_id')
    is_purchased = request.json.get('is_purchased')

    if item_id is None or is_purchased is None:
        return dict(error="Item ID and purchased status are required.")

    # Update item status and set checked_on timestamp if purchased
    db((db.shopping_list.id == item_id) & (db.shopping_list.user_email == user_email)).update(
        is_purchased=is_purchased,
        checked_on=get_time() if is_purchased else None
    )
    return dict(message="Item status updated.")

@action('delete_item', method='POST')
@action.uses(db, auth.user)
def delete_item():
    user_email = get_user_email()
    item_id = request.json.get('item_id')

    if not item_id:
        return dict(error="Item ID is required.")

    # Delete item only if it belongs to the current user
    db((db.shopping_list.id == item_id) & (db.shopping_list.user_email == user_email)).delete()
    return dict(message="Item deleted.")
