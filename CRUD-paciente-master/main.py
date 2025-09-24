# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Patient(BaseModel):
    id: int
    name: str
    age: int
    disease: str

patients = []

@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.get("/patients/", response_model=List[Patient])
def get_patients():
    return patients

@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated_patient: Patient):
    for i, patient in enumerate(patients):
        if patient.id == patient_id:
            patients[i] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}", response_model=Patient)
def delete_patient(patient_id: int):
    for i, patient in enumerate(patients):
        if patient.id == patient_id:
            return patients.pop(i)
    raise HTTPException(status_code=404, detail="Patient not found")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
