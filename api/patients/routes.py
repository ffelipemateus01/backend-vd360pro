from fastapi import APIRouter, HTTPException
from api.patients.models import Patient
from api.patients.service import create_patient_service, get_all_patients_service, get_patient_by_id_service, count_patients_service

router = APIRouter()

@router.post('/create', response_model=Patient)
async def create_patient(new_patient:Patient):
    patient = create_patient_service(new_patient)
    return patient
    
@router.get('/list/offset={offset}')
async def list_patients(offset: int):
    if offset < 0:
        print(f'Offset da lista de paciente precisa ser maior ou igual a ZERO. ({offset})')
        raise HTTPException(status_code=400, detail=f'Offset da lista de paciente precisa ser maior ou igual a ZERO. ({offset})')
    patients = get_all_patients_service(offset)
    return patients
    
@router.get('/id={id}')
async def get_patient_by_id(id: int):
    if id < 0:
        print(f'Id do paciente precisa ser maior ou igual a ZERO. ({id})')
        raise HTTPException(status_code=400, detail=f'Id do paciente precisa ser maior ou igual a ZERO. ({id})')
    patient = get_patient_by_id_service(id)
    return patient
    
@router.get('/count')
async def count_patients():
    n_patients = count_patients_service()
    return n_patients
