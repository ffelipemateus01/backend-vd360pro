from fastapi import APIRouter
from api.io.sivecplus.service import start_sivec_service, close_sivec_service, start_record_service, pause_record_service, send_command_service

router = APIRouter()

@router.post('/connect/port_name={port_name}')
async def connect_serial(port_name: str):
    port_name = port_name.lower()
    start_sivec_service(port_name)
    return{'Status:', f'Sivec: Conectado com sucesso a porta {port_name}'}
    
@router.post('/record_on')
async def start_record():
    start_record_service()
    return{'Status:', f'Sivec: Gravação iniciada com sucesso.'}
    
@router.post('/record_off')
async def pause_record():
    pause_record_service()
    return{'Status:', f'Sivec: Gravação interrompida com sucesso.'}
    
@router.post('/send/to/port_name={port_name}/command={command}')
async def send_command(port_name: str, command: str):
    port_name = port_name.lower()
    command = command.lower()
    send_command_service(port_name, command)
    return{'Status:', f'Sivec: Comando {command} enviado com sucesso pela serial.'}

@router.post('/close/port_name={port_name}')
async def close_serial(port_name: str):
    port_name = port_name.lower()
    close_sivec_service(port_name)
    return{'Status:', f'Sivec: Conexão com a porta {port_name} encerrada com sucesso.'}