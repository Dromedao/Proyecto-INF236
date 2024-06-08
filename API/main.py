from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
import uvicorn
from config.database import Session, engine, Base
from models.search import Search as SearchModel
from models.contact import Contact as ContactModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from browser import caller

from scrape_form import scrapeDataFromSpreadsheet

from send_email import send_email

"""
Matías Leonardo Guerra Valles
Joaquin Alejandro Lopez Diaz
Sebastian Ignacio Torrealba Catalan
Joaquin Antonio Veliz Carmona
"""

app = FastAPI()

Base.metadata.create_all(bind=engine)

class Search(BaseModel):
    prompt : str

class Workshopper(BaseModel):
    name : str
    email : str
    type_of: str
    state : int
    decision : int

@app.get('/')
def read_root():
    return {"welcome": "Welcome to Apprende API"}

@app.get("/search/{id}", status_code=status.HTTP_200_OK)
def get_by_id(id: int):
    db = Session()
    result = db.query(SearchModel).filter(SearchModel.id == id).first()
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    return JSONResponse(status_code=status.HTTP_404_OK, content={id:"No se encuentra en la base de datos..."})

@app.get("/searchs", status_code=status.HTTP_200_OK)
def get_all_search():
    db = Session()
    result = db.query(SearchModel).all()
    if result is not None:
        for item in result:
            item.budget = "http://localhost:8000/budget/" + str(item.id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    return JSONResponse(status_code=status.HTTP_204_OK, content={"response": "La base de datos se encuentra vacia..."})

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
    call = caller(search.prompt)
    searchRequest = {"workshoppers" : call["workshoppers"]}
    db = Session()
    aux = {"prompt": search.prompt}
    aux.update(searchRequest)
    new_search = SearchModel(**aux)
    db.add(new_search)
    db.commit()
    return {"workshoppers": searchRequest["workshoppers"], "type_of": call["type_of"]}

@app.get("/contacts", status_code=status.HTTP_200_OK)
def get_all_contacts():
    db = Session()
    result = db.query(ContactModel).all()
    if result is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    return JSONResponse(status_code=status.HTTP_204_OK, content={"response": "La base de datos se encuentra vacia..."})

@app.post("/contact")
def contact(workshopper: Workshopper):
    db = Session()
    aux = {"name": workshopper.name, "email": workshopper.email, "type_of": workshopper.type_of,"state": workshopper.state, "decision": workshopper.decision}
    new_contact = ContactModel(**aux)
    db.add(new_contact)
    db.commit()

@app.patch("/contact_decision")
def contact_accept(workshopper: Workshopper):
    db = Session()
    existing_contact = db.query(ContactModel).filter_by(email=workshopper.email).first()
    
    if existing_contact:
        if isinstance(workshopper.state, str) or isinstance(workshopper.decision, str):
            raise HTTPException(status_code=422, detail="Los campos state y decision deben ser enteros")
        
        existing_contact.decision = workshopper.decision
        db.commit()
        return {"message": f"Decision updated to {workshopper.decision} for email: {workshopper.email}"}
    
    raise HTTPException(status_code=404, detail="Contact not found")
        
@app.get("/send_email")
def sender_email(workshopper: Workshopper):
    if isinstance(workshopper.state, str) or isinstance(workshopper.decision, str):
        raise HTTPException(status_code=422, detail="Los campos state y decision deben ser enteros")

    send_email_result = send_email("matiasguerravalles@gmail.com", workshopper.name)
    if send_email_result == 1:  # En caso de éxito
        return {"message": f"Email sent to {workshopper.name}"}
    return {"message": f"Error sending the email to {workshopper.name}"}

@app.get("/scrape_form")
def scrape_form():
    try:
        scrape = scrapeDataFromSpreadsheet()
        return {"results": scrape}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)