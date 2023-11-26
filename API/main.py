from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
import uvicorn
from config.database import Session, engine, Base
from models.search import Search as SearchModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from browser import caller

"""
Grupo 9
Joaquín Lopez
Matías Guerra
"""

app = FastAPI()

Base.metadata.create_all(bind=engine)

class Search(BaseModel):
    prompt : str

@app.get('/')
def read_root():
    return {"welcome": "Welcome to Apprende API"}

@app.get("/search", status_code=status.HTTP_200_OK)
def get_by_id():
    db = Session()
    result = db.query(SearchModel).filter(SearchModel.id == 1).first()
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={1:"No se encuentra en la base de datos..."})

@app.get("/search/{id}", status_code=status.HTTP_200_OK)
def get_by_id(id: int):
    db = Session()
    result = db.query(SearchModel).filter(SearchModel.id == id).first()
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={id:"No se encuentra en la base de datos..."})

@app.get("/searchs", status_code=status.HTTP_200_OK)
def get_all_search():
    db = Session()
    result = db.query(SearchModel).all()
    if result is not None:
        for item in result:
            item.budget = "http://localhost:8000/budget/" + str(item.id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"response": "La base de datos se encuentra vacia..."})

@app.get("/budget")
def get_budget():
    db = Session()
    result = db.query(SearchModel).filter(SearchModel.id == 1).first()
    if result is not None:
        total = 0
        for element in jsonable_encoder(result)["materials"][1]:
            try:
                total += int(element[1].replace(".","").replace("$",""))
            except:
                total = "No se puede calcular para el caso..."
                break
        aux = dict(jsonable_encoder(result))
        aux = {"id": 1,"budget": total}
    aux = {1: "No se encuentra en la base de datos..."}
    return JSONResponse(status_code=status.HTTP_200_OK, content=aux) 

@app.get("/budget/{id}")
def get_budget_id(id: int):
    db = Session()
    result = db.query(SearchModel).filter(SearchModel.id == id).first()
    if result is not None:
        total = 0
        for element in jsonable_encoder(result)["materials"][1]:
            try:
                total += int(element[1].replace(".","").replace("$",""))
            except:
                total = "No se puede calcular para el caso..."
                break
        aux = dict(jsonable_encoder(result))
        aux = {"id": aux["id"],"budget": total}
    else:
        aux = {id: "No se encuentra en la base de datos..."}
    return JSONResponse(status_code=status.HTTP_200_OK, content=aux)

@app.post('/search', status_code=status.HTTP_201_CREATED)
def busqueda(search: Search):
    searchRequest = caller(search.prompt)
    db = Session()
    aux = {"prompt": search.prompt}
    aux.update(searchRequest)
    new_search = SearchModel(**aux)
    db.add(new_search)
    db.commit()
    return {"workshoppers": searchRequest["workshoppers"], "materials":searchRequest["materials"]}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)