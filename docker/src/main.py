from fastapi import FastAPI

api = FastAPI(
    title='My API'
)

@api.get('/')
def get_index():
    return {'data': 'hello world'}
    #return "Hello world"

@api.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }

"""
@api.get('/item/{itemid}')
def get_item(itemid):
    return {
        'route': 'dynamic',
        'itemid': itemid
        }
"""

@api.get('/item/{itemid:float}')
def get_item_float(itemid):
    return {
        'route': 'dynamic',
        'itemid': itemid,
        'source': 'float'
    }

@api.get('/item/{itemid}')
def get_item_default(itemid):
    return {
        'route': 'dynamic',
        'itemid': itemid,
        'source': 'string'
    }

@api.get('/item/{itemid}/description/{language}')
def get_item_language(itemid, language):
    if language == 'fr':
        return {
            'itemid': itemid,
            'description': 'un objet',
            'language': 'fr'
        }
    else:
        return {
            'itemid': itemid,
            'description': 'an object',
            'language': 'en'
        }