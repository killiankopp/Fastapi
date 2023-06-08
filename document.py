from fastapi import FastAPI
from fastapi import Header
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime
import time
import asyncio

api = FastAPI(
    title="My API",
    description="My own API powered by FastAPI.",
    version="1.0.1",
    openapi_tags=[
        {
            'name': 'home',
            'description': 'default functions'
        },
        {
            'name': 'items',
            'description': 'functions that are used to deal with items'
        }
    ])

class MyException(Exception):
    def __init__(self,
                 name : str,
                 date: str):
        self.name = name
        self.date = date

@api.exception_handler(MyException)
def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )


class Computer(BaseModel):
    """a computer that is available in the store
    """
    computerid: int
    cpu: Optional[str]
    gpu: Optional[str]
    price: float

@api.get('/', name='hello world', tags=['home'])
def get_index():
    """Returns greetings
    """
    return {'greetings': 'welcome'}

@api.put('/computer', name='Create a new computer', tags=['home', 'items'])
def get_computer(computer: Computer):
    """Creates a new computer within the database
    """
    return computer

@api.get('/custom', name='Get custom header')
def get_content(custom_header: Optional[str] = Header(None, description='My own personal header')):
    return {
        'Custom-Header': custom_header
    }

data = [1, 2, 3, 4, 5]

@api.get('/data')
def get_data(index):
    try:
        return {
            'data': data[int(index)]
        }
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )

@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
      name='my error',
      date=str(datetime.datetime.now())
      )

responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

@api.get('/thing', responses=responses)
def get_thing():
    return {
        'data': 'hello world'
    }

def wait_sync():
    time.sleep(10)
    return True


async def wait_async():
    await asyncio.sleep(10)
    return True


@api.get('/sync')
def get_sync():
    wait_sync()
    return {
        'message': 'synchronous'
    }


@api.get('/async')
async def get_async():
    wait_async()
    return {
        'message': 'asynchronous'
    }