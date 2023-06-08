import pandas as pd
import random
from typing import Optional
from pydantic import BaseModel

df = pd.read_csv('questions.csv')
df = df.fillna('null')
# correction "Sytèmes distribués" en "Systèmes distribués"
df['subject'] = df['subject'].replace('Sytèmes distribués', 'Systèmes distribués')

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

# Victor = nettoyeur
def victor(sales):
    propres = []
    
    for sale in sales:
        t = sale.strip()
        t = t.replace('"', '')
        propres.append(t)   

    return propres

class Question:
    def __init__(self, question, subject, use, correct, responseA, responseB, responseC, responseD, remark):
        self.question = question
        self.subject = subject
        self.use = use
        self.correct = correct
        self.responseA = responseA
        self.responseB = responseB
        self.responseC = responseC
        self.responseD = responseD
        self.remark = remark

    def __str__(self):
        return f"{self.question} {self.answer}"
    
    def uses(subject): 
        uses = []
        df_use = df

        if (subject != None):
            subjects = subject.split(",")
            subjects = victor(subjects)
            df_use = df_use[df['subject'].isin(subjects)]

        uses = df_use['use'].unique()
        uses = uses.tolist()
        return uses
    
    def subjects(use): 
        subjects = []
        df_subject = df

        if (use != None):
            df_subject = df_subject[df['use'] == use]
            
        subjects = df_subject['subject'].unique()
        subjects = subjects.tolist()
        return subjects
    
    def piocher(nb, use, subject):
        df_pioche = df

        if (use != None):
            df_pioche = df_pioche[df_pioche['use'] == use]

        if (subject != None):
            subjects = subject.split(",")
            subjects = victor(subjects)
            df_pioche = df_pioche[df_pioche['subject'].isin(subjects)]

        selection = {}                      # dictionnaire des index questions sélectionnées
        nb_lignes = df_pioche.shape[0]      # nombre de lignes du dataframe
        i = [i for i in range(nb_lignes)]   # tableau temporaire des index
        
        # on ne peut pas piocher plus de questions que le nombre de questions disponibles
        nb = nb if nb < nb_lignes else nb_lignes
        
        for j in range(nb):
            # choix d'un index au hasard
            x = random.randint(0, len(i) - 1)

            # récupération de la question
            question = df_pioche.iloc[x,:]
            question = question.to_dict()
            selection[j] = question

            # suppression de l'index pour ne pas le repiocher
            i.pop(x)

        return selection
    
    def add(question: QuestionModel):
        oQuestion = Question(question.question, question.subject, question.use, question.correct, question.responseA, question.responseB, question.responseC, question.responseD, question.remark)
        df.loc[len(df)] = oQuestion.__dict__
        df.to_csv('questions.csv', index=False)
        return oQuestion
        