from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from api.patients.routes import router as patients_router
from api.io.sivecplus.routes import router as sivec_router
from api.io.oto.routes import router as oto_router
from api.io.cameras.routes import router as cameras_router
from api.controls.flowchart.routes import router as flowchart_router
from core.exceptions import SivecError, SivecIndexError, OtoError, OtoIndexError, PatientDbError, PatientNotFound, SivecRepositoryError

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=patients_router, prefix='/patients', tags=['Patients'])
app.include_router(router=cameras_router, prefix='/cameras', tags=['Cameras'])
app.include_router(router=sivec_router, prefix='/sivecplus', tags=['Sivec Plus'])
app.include_router(router=oto_router, prefix='/oto', tags=['Otocalorimeter'])
app.include_router(router=flowchart_router, prefix='/flowchart', tags=['Flowchart'])

@app.exception_handler(OtoError)
async def oto_exception_handler(request: Request, exc: OtoError):
    return JSONResponse(
        status_code=503,
        content={'detail': f'{exc}'})

@app.exception_handler(OtoIndexError)
async def oto_index_exception_handler(request: Request, exc: OtoIndexError):
    return JSONResponse(
        status_code=404,
        content={'detail': f'{exc}'})

@app.exception_handler(SivecError)
async def sivec_exception_handler(request: Request, exc: SivecError):
    return JSONResponse(
        status_code=503,
        content={'detail': f'{exc}'})

@app.exception_handler(SivecIndexError)
async def sivec_index_exception_handler(request: Request, exc: SivecIndexError):
    return JSONResponse(
        status_code=404,
        content={'detail': f'{exc}'})

@app.exception_handler(SivecRepositoryError)
async def sivec_repository_exception_handler(request: Request, exc: SivecRepositoryError):
    return JSONResponse(
        status_code=503,
        content={'detail': f'{exc}'})

@app.exception_handler(PatientNotFound)
async def patient_notfound_exception_handler(request: Request, exc: PatientNotFound):
    return JSONResponse(
        status_code=404,
        content={'detail': f'{exc}'})

@app.exception_handler(PatientDbError)
async def patient_dberror_exception_handler(request: Request, exc: PatientDbError):
    return JSONResponse(
        status_code=503,
        content={'detail': f'{exc}'})

@app.get("/")
def root():
    return {"Status": "API online"}