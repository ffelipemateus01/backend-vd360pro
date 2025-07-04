from fastapi import APIRouter, HTTPException
from api.io.sivecplus.service import start_serial_service, close_serial_service, start_record_service, pause_record_service, send_command_service

router = APIRouter()

@router.post('/connect/port_name={port_name}')
async def connect_serial(port_name: str):
    try:
        start_serial_service(port_name)
        return{'Status:', f'Serial: Conectado com sucesso a porta {port_name}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serial: Problema ao se conectar com a porta serial.{e}')
    
@router.post('/record_on')
async def start_record():
    try:
        start_record_service()
        return{'Status:', f'Serial: Gravação iniciada com sucesso.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serial: Problema ao iniciar a gravação.{e}')
    
@router.post('/record_off')
async def pause_record():
    try:
        pause_record_service()
        return{'Status:', f'Serial: Gravação interrompida com sucesso.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serial: Problema ao pausar a gravação.{e}')
    
@router.post('/send/to/port_name={port_name}/command={command}')
async def send_command(port_name: str, command: str):
    try:
        send_command_service(port_name, command)
        return{'Status:', f'Serial: Comando {command} enviado com sucesso pela serial.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serial: Problema ao tentar enviar um comando pela porta serial.{e}')

@router.post('/close/port_name={port_name}')
async def close_serial(port_name: str):
    try:
        close_serial_service(port_name)
        return{'Status:', f'Serial: Conexão com a porta {port_name} encerrada com sucesso.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Serial: Problema ao tentar encerrar a conexão com a porta serial.{e}')