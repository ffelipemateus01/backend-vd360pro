from fastapi import APIRouter, HTTPException
from api.patients.models import Patient
from api.patients.service import insert_paciente, get_all_pacientes, get_paciente_by_id, count_pacientes

router = APIRouter()

@router.post('/create', response_model=Patient)
async def cadastrar_paciente(paciente:Patient):
    try:
        paciente_inserido = insert_paciente(paciente)
        if paciente_inserido is None:
            raise HTTPException(status_code=400, detail="Erro ao inserir paciente")
        return paciente_inserido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
    
@router.get('/list/offset={offset}')
async def listar_pacientes(offset: int):
    try:       
        list_pacientes = get_all_pacientes(offset)
        if list_pacientes is None:
            raise HTTPException(status_code=400, detail="Erro ao listar os pacientes")
        return list_pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
    
@router.get('/id={id}')
async def buscar_paciente_por_id(id: int):
    try:
        paciente = get_paciente_by_id(id)
        if paciente is None:
            raise HTTPException(status_code=400, detail="Erro ao buscar o paciente")
        return paciente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
    
@router.get('/count')
async def quantidade_pacientes():
    try:
        n_pacientes = count_pacientes()
        if n_pacientes is None:
            raise HTTPException(status_code=400, detail="Erro ao contar os pacientes")
        return n_pacientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
