from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.patients.routes import router as patients_router
from api.io.sivecplus.routes import router as sivec_router
from api.io.cameras.routes import router as cameras_router
from api.controls.flowchart.routes import router as flowchart_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=patients_router, prefix='/patients', tags=['Patients'])
app.include_router(router=cameras_router, prefix='/cameras', tags=['Cameras'])
app.include_router(router=sivec_router, prefix='/sivecplus', tags=['SivecPlus'])
app.include_router(router=flowchart_router, prefix='/flowchart', tags=['Flowchart'])

@app.get("/")
def root():
    return {"Status": "API online"}