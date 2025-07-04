from fastapi import APIRouter, HTTPException
from api.io.oto.service import start_oto_service, close_oto_service

router = APIRouter()

@router.post('/connect/port_name={port_name}')
async def connect_serial(port_name: str):
    port_name = port_name.lower()
    try:
        start_oto_service(port_name)
        return{'Status:', f'Otocalorímetro: Conexão com a porta {port_name} encerrada com sucesso.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Otocalorímetro: Problema ao tentar conectar com a porta {port_name}. {e}')
    
@router.post('/close/port_name={port_name}')
async def close_serial(port_name: str):
    port_name = port_name.lower()
    try:
        close_oto_service(port_name)
        return{'Status:', f'Otocalorímetro: Conexão com a porta {port_name} encerrada com sucesso.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Otocalorímetro: Problema ao tentar encerrar a conexão com a porta serial.{e}')