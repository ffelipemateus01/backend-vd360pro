from fastapi import APIRouter, HTTPException, WebSocket
from api.io.cameras.models import CameraInput
from api.io.cameras.service import init_camera

router = APIRouter()

@router.post('/set_camera')
async def set_camera(camera:CameraInput):
    try:
        init_camera(*camera.camera)
        return {'Status': 'Camera {} configurada'.format(camera.camera[1])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao configurar câmeras: {e}")
    
@router.websocket('/ws/frames')
async def ws_endpoint(websocket: WebSocket):
    print("Cliente tentando conectar ao WebSocket")