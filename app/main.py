from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import bb84_router

app = FastAPI(title="BB84 Quantum Key Distribution API", version="1.0")

app.include_router(bb84_router.router)

# Configurar CORS
origins = [
    "http://localhost:4200",  # tu frontend Angular
    "http://127.0.0.1:4200" # también si lo necesitas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],     # Authorization, Content-Type, etc.
)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Protocolo BB84"}