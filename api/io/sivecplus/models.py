from pydantic import BaseModel

class Data(BaseModel):
    electrode_1: int = 0
    electrode_2: int = 0
    electrode_3: int = 0
    gyroscope_x: int = 0
    gyroscope_y: int = 0
    gyroscope_z: int = 0

class DataFormatted(BaseModel):
    g_electrode_1: float = 0.0
    g_electrode_2: float = 0.0
    g_electrode_3: float = 0.0
    g_gyroscope_x: float = 0.0
    g_gyroscope_y: float = 0.0
    g_gyroscope_z: float = 0.0
