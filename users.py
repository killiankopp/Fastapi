from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    itemid: int
    description: str
    owner: Optional[str] = None
    other: Optional[str] = None

api = FastAPI(
    title='Users API'
)

users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]

def get_user_from_id(userid):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return user
    except IndexError:
        return {}

@api.get('/')
def get_index():
    return {'data': 'hello world'}

@api.get('/users')
def get_users():
    return users_db

@api.get('/users/{userid}')
def get_users_id(userid:int, autre: Optional[str] = None):
    user = get_user_from_id(userid)
    return user

@api.get('/users/{userid}/name')
def get_users_name(userid:int):
    user = get_user_from_id(userid)
    if user['name']:
        return user['name']
    else:
        return "User not found"

@api.get('/users/{userid}/subscription')
def get_users_description(userid:int):
    user = get_user_from_id(userid)
    if user['subscription']:
        return user['subscription']
    else:
        return "User not found"

# ici on va utiliser le modèle Item
@api.post('/item')
def post_item(item: Item):
    return {
        'retour': item.other
    }