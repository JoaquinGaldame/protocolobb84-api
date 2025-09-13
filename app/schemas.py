from pydantic import BaseModel
from typing import List, Optional

class BB84Request(BaseModel):
    largo: int = 16
    con_espia: bool = False

class BB84Response(BaseModel):
    baseAna: List[str]
    baseBeto: List[str]
    bitsAna: List[int]
    bitsBeto: List[int]
    claveCompartida: List[int]
    porcentaje: float
    baseEva: Optional[List[str]] = None
    bitsBetoEva: Optional[List[int]] = None
    claveConEva: Optional[List[int]] = None
    porcentajeConEva: Optional[float] = None