from api.patients.repository import create_patient, get_all_patients, get_patient_by_id, count_patients
from api.patients.models import Patient

def create_patient_service(patient: Patient) -> Patient | None:
    return create_patient(patient)

def get_all_patients_service(offset: int):
    return get_all_patients(offset)

def get_patient_by_id_service(id: int) -> Patient | None:
    return get_patient_by_id(id)

def count_patients_service() -> int | None:
    return count_patients()