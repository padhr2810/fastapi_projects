
"""
GOOD
http http://127.0.0.1:8000
http http://127.0.0.1:8000/patients/TimmyOToole
http http://127.0.0.1:8000/disease/diabetes
http http://127.0.0.1:8000/disease/chf

ERRORS
http http://127.0.0.1:8000/patients
http http://127.0.0.1:8000/disease/Diabetes

"""

from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class DiseaseType(str, Enum):
    DIABETES = "diabetes"
    CHF = "chf"

@app.get("/")
async def empty_request():
    return {"Please specify a patient": "Thank you!"}


@app.get("/patients/{id}")
async def get_patient(id: str):
    return {"id": id}

# When add an extra Path parameter a different function gets called here.
@app.get("/patients/{id}/{county}")
async def get_patient(id: str, county: str):
    return {"id": id, "county": county}

hospitals = {"1": "Brigham", "2": "MGH"}

@app.get("/hospitals")
async def get_hospital():
    return hospitals

@app.get("/disease/{disease}")
async def get_patients(disease: DiseaseType):
    if disease == "diabetes": 
        px_sublist = ["diabetic_guy_1", "diabetic_guy_2"]
    elif disease == "chf":
        px_sublist = ["chf_guy_1", "chf_guy_2"] 
    
    return {disease: px_sublist}



