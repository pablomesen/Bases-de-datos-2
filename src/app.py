# Inicia la RestAPI, la DB, define las rutas y permite su acceso desde cualquier origen.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, posts
from .db import DBInstance

app = FastAPI(title="TC01", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la TC01 de BD2! :)    Accede a /docs para ver la documentación de endpoints."}

# Crea las tablas definidas en los modelos antes de iniciar la aplicación
DBInstance.Base.metadata.create_all(bind=DBInstance.engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)