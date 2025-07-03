from fastapi import APIRouter, HTTPException
from api.controls.flowchart.service import altera_fluxograma
from api.controls.flowchart.models import Flowchart

router = APIRouter()

@router.post('/save')
async def altera_fluxo():
    try:
        flow = altera_fluxograma()
        return {'sucesso amigo'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")
