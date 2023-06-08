from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from typing import Optional
from pydantic import BaseModel
from question import Question
from user import *

messages = {
    'error_401': 'Vous devez être connecté pour accéder à cette ressource.',
    'error_403': "Vous n'avez pas les droits suffisants pour accéder à cette ressource."
    }

api = FastAPI(
    title="Questionnaire",
    description="API de gestion d'un questionnaire. Génération de QCM à partir d'une 'base de données' de questions. Il est possible de créer un QCM de 5, 10 ou 20 questions.",
    version="1.0.1",
    openapi_tags=[
        {
            'name': 'QCM',
            'description': "routes d'utilisation du QCM"
        },
        {
            'name': 'admin',
            'description': "routes permettant d'administrer les questions"
        }
    ])

class QuestionModel(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None
    remark: Optional[str] = None

@api.get('/uses', name='Uses', tags=['QCM'])
async def get_uses(username: Annotated[str, Depends(login)], subject: str = None):
    """Retourne les uses possibles. Vous pouvez filtrer les uses en fonction d'un (ou plusieurs) subject(s). Les sujets sont séparés par une virgule.
    """
    uses = Question.uses(subject)
    return JSONResponse(content=uses)

@api.get('/subjects', name='Subjects', tags=['QCM'])
async def get_subjects(username: Annotated[str, Depends(login)], use: str = None):
    """Retourne les subjects possibles
    """
    subjects = Question.subjects(use)
    return JSONResponse(content=subjects)

@api.get('/questions', name='Questions', tags=['QCM'])
async def get_questions(username: Annotated[str, Depends(login)], nb: int = 5, use: str = None, subject: str = None):
    """Retourne une série de questions piochées au hasard. Si le nombre de questions demandées est supérieur au nombre de questions disponibles, toutes les questions sont retournées.
    """
    questions = Question.piocher(nb, use, subject)
    return JSONResponse(content=questions)
    
@api.get('/me', name='Me', tags=['QCM'])
async def get_me(username: Annotated[str, Depends(login)]):
    """Retourne le nom de l'utilisateur connecté
    """
    return JSONResponse(content=username)

@api.post('/question', name='Question', tags=['admin'])
def post_item(username: Annotated[str, Depends(login)], question: QuestionModel):
    if username != 'admin':
        raise HTTPException(status_code=401, detail=messages['error_403'])
    oQuestion = Question.add(question)
    return {
        'retour': oQuestion.question
    }