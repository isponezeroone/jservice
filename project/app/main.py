from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
import json
from sqlalchemy import select, engine

import requests 

from bs4 import BeautifulSoup

from urllib import request


from sqlalchemy.orm import sessionmaker

#Создаем базу данных

DATABASE_URL='postgresql://postgres:postgres@db:5432/foo'


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

questions = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column("question", sqlalchemy.String),
    sqlalchemy.Column("answer", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL,pool_size=100, max_overflow=0)

metadata.create_all(engine)


#Создаем FastAPI
app = FastAPI()

#Аннотируем типы входных и выходных данных
class Ques_num(BaseModel):
    questions_num: int

    
class Question(BaseModel):
    question: str

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/questions/', response_model=List[Question])
async def read_questions():
    query = questions.select()
    return await database.fetch_all(query)

#Выполняет цикл заданное questions_num количество раз
@app.post("/questions/", response_model=Question)
async def create_question(questions_num: Ques_num):
    i=1
    while i<=int(f'{questions_num.questions_num}'):
        url = f'https://jservice.io/api/random?count=1'       	
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html,'html.parser')
        site_json=json.loads(soup.text)
        
        s = select(questions.c.question)
        result = engine.execute(s).fetchall()
        #Если предыдущий вопрос в БД отсутствует, то выводим пустую строку. В остальных случаях выводим предыдущий вопрос        
        if len(result)==0:
            last_question=""
        else: 
            Session = sessionmaker(bind = engine)
            session = Session()
            last_question=session.query(questions).order_by(questions.c.id.desc()).first()
            last_question=str(last_question['question'])
        #Проверяем уникальность вопроса
        if site_json[0]['question'] in list(result):
            continue
        query = questions.insert().values(question=site_json[0]['question'],answer=site_json[0]['answer'], date=site_json[0]['airdate'])
        last_record_id = await database.execute(query)
        i+=1
    return Question(question=last_question)


