from fastapi import APIRouter
from app.bb84 import BB84RealSimulator
from app.schemas import BB84Request, BB84Response

router = APIRouter(prefix="/bb84", tags=["BB84"])

@router.post("/simular", response_model=BB84Response)
def simular(request: BB84Request):
    simulator = BB84RealSimulator(largo=request.largo, con_espia=request.con_espia)
    return simulator.run()