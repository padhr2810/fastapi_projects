
"""
GOOD
http http://127.0.0.1:8000
http http://127.0.0.1:8000/patients/TimmyOToole

ERRORS
http http://127.0.0.1:8000/patients

"""

from fastapi import FastAPI

app = FastAPI()

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


