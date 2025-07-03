# from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
# from fastapi.responses import RedirectResponse
# from pydantic import BaseModel
# from typing import Dict
# from contextlib import asynccontextmanager
# from recorder import VideoRecorder

# class CameraInput(BaseModel):
#     cameras: Dict[str, int]

# video_recorder = VideoRecorder()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     #video_recorder.start()
#     yield
#     video_recorder.stop()

# app = FastAPI(lifespan=lifespan)

# @app.get("/")
# async def redirect_to_docs():
#     return RedirectResponse(url="/docs")

# @app.post("/set_camera")
# async def set_camera(data: CameraInput):
#     try:
#         for camera_id, device_index in data.cameras.items():
#             video_recorder.set_camera(int(camera_id), int(device_index))
#         return {"status": "Câmeras configuradas"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Erro ao configurar câmeras: {e}")

# @app.post("/start")
# async def start_recording():
#     video_recorder.start_recording()
#     return {"status": "Gravação iniciada"}

# @app.post("/pause")
# async def pause_recording():
#     video_recorder.pause_recording()
#     return {"status": "Gravação pausada"}

# @app.post("/finalize")
# async def finalize_recording():
#     video_recorder.stop_recording()
#     return {"status": "Gravação finalizada"}

# @app.post("/new_file")
# async def new_file():
#     video_recorder.new_file()
#     return {"status": "Novo arquivo criado"}

# @app.post("/disconnect")
# async def disconnect():
#     video_recorder.disconnect()
#     return {"status": "Desconectado"}

# @app.websocket("/ws/frames")
# async def websocket_endpoint(websocket: WebSocket):
#     print("Cliente tentando conectar ao WebSocket")
#     await websocket.accept()
#     print("Cliente WebSocket conectado")

#     video_recorder.running = True
#     try:
#         await video_recorder.run(websocket)
#     except WebSocketDisconnect:
#         print("Cliente WebSocket desconectado")
#     except Exception as e:
#         print(f"Erro no WebSocket: {e}")
#     finally:
#         video_recorder.websocket = None
#         await websocket.close()
#         print("WebSocket fechado")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)