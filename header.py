from fastapi import FastAPI
from fastapi import Header

api = FastAPI(
    title='Header API'
)

@api.get('/headers')
def get_headers(user_agent=Header(None)):
    return {
        'User-Agent': user_agent
    }

@api.get('/headerstest')
def get_headerstest(test=Header(None)):
    return {
        'test': test
    }

@api.get('/autre')
def get_autre():
    user_agent=Header(None)
    return user_agent