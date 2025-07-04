from pydantic import BaseModel, field_validator

class ElectrodeCalibration(BaseModel):
    base_line_1: int = 0
    base_line_2: int = 0
    base_line_3: int = 0
    bytes_by_degrees_1: int = 1
    bytes_by_degrees_2: int = 1
    bytes_by_degrees_3: int = 1

    @field_validator('bytes_by_degrees_1')
    def check_bytes_by_desgrees_1(cls, bytes_by_degrees_1: int):
        if bytes_by_degrees_1 <= 0:
            raise ValueError("Valores inválidos na calibração dos eletrodos.")
        return bytes_by_degrees_1
    
    @field_validator('bytes_by_degrees_2')
    def check_bytes_by_desgrees_2(cls, bytes_by_degrees_2: int):
        if bytes_by_degrees_2 <= 0:
            raise ValueError("Valores inválidos na calibração dos eletrodos.")
        return bytes_by_degrees_2
    
    @field_validator('bytes_by_degrees_3')
    def check_bytes_by_desgrees_3(cls, bytes_by_degrees_3: int):
        if bytes_by_degrees_3 <= 0:
            raise ValueError("Valores inválidos na calibração dos eletrodos.")
        return bytes_by_degrees_3

class GyroscopeCalibration(BaseModel):
    offset_x: int = 0
    offset_y: int = 0
    offset_z: int = 0
    convert_constant: float = 1.0

    @field_validator('convert_constant')
    def check_bytes_by_desgrees_3(cls, convert_constant: float):
        if convert_constant <= 0:
            raise ValueError("Valores inválidos na calibração do giroscópio.")
        return convert_constant