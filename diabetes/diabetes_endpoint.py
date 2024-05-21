
"""
HTTPie CALLS
http http://127.0.0.1:8000
http http://127.0.0.1:8000/patients/TimmyOToole
http http://127.0.0.1:8000/patients/TimmyOToole/donegal
http http://127.0.0.1:8000/disease/diabetes
http http://127.0.0.1:8000/disease/chf
http http://127.0.0.1:8000/hospitals
http --form POST http://localhost:8000/filesbytes  file@./data.csv
http --form POST http://localhost:8000/fileslarge  file@./data.csv
http http://127.0.0.1:8000/mri_brain


ILLUSTRATIVE ERRORS
http http://127.0.0.1:8000/patients
http http://127.0.0.1:8000/disease/Diabetes

"""

from fastapi import FastAPI
from fastapi import File 
from fastapi import UploadFile
from fastapi import Path
from fastapi.responses import FileResponse
import io 
from enum import Enum
import pandas as pd 

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


# Upload a CSV file for analysis: Method 1
@app.post("/filesbytes")
async def upload_file(file: bytes = File(...)):

    df = pd.read_csv(io.BytesIO(file), encoding='utf8')
    cols = list(df.columns)
    hba1c = df["hba1c"].mean()

    return {"columns": cols, "mean_hba1c": hba1c }

# Upload a CSV file for analysis: Method 2
# PANDAS INPUT DIFFERS DEPENDING ON WHETHER BYTES OR FILE UPLOAD.
@app.post("/fileslarge")
async def upload_file(file: UploadFile = File(...)):
   
    df = pd.read_csv(file.file)
    cols = list(df.columns)
    hba1c = df["hba1c"].mean()

    return {"columns": cols, "mean_hba1c": hba1c }

# Download an image.
# Open endpoint in browser to view the MRI image (not in terminal)
@app.get("/mri_brain")
async def get_mri():
    #root_dir = Path(__file__).parent.parent
    #picture_path = root_dir / "assets" / "mri_brain.jpg"
    picture_path = "assets/mri_brain.jpg"
    return FileResponse(picture_path)
    
