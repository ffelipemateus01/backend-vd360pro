from fastapi import APIRouter
from api.io.oto.service import start_oto_service, close_oto_service, increase_temp_service, decrease_temp_service

router = APIRouter()

@router.post('/connect/port_name={port_name}')
async def connect_serial(port_name: str):
    port_name = port_name.lower()
    start_oto_service(port_name)
    return{'Status:', f'Otocalorímetro: Conexão com a porta {port_name} encerrada com sucesso.'}
    
@router.post('/close/port_name={port_name}')
async def close_serial(port_name: str):
    port_name = port_name.lower()
    close_oto_service(port_name)
    return{'Status:', f'Otocalorímetro: Conexão com a porta {port_name} encerrada com sucesso.'}
    
@router.post('/increase')
async def increase_temp(port_name: str):
    port_name = port_name.lower()
    increase_temp_service(port_name)
    return {'Status':'Otocalorímetro: Temperatura aumentada.'}
    
@router.post('/decrease')
async def decrease_temp(port_name: str):
    port_name = port_name.lower()
    decrease_temp_service(port_name)
    return {'Status':'Otocalorímetro: Temperatura reduzida.'}