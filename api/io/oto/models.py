from pydantic import BaseModel

class OtoData(BaseModel):
    set_point: int = 24
    sensor_irr: float = 0.0
    sensor_amb: float = 0.0