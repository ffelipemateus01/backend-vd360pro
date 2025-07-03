from pydantic import BaseModel
from typing import Tuple

class CameraInput(BaseModel):
    camera: Tuple[str,int] 