from fastapi import FastAPI
from config.database import Base, engine
from .routers import clientes, movimientos

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(clientes.router)
app.include_router(movimientos.router)