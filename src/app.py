# Este código se encarga definir las rutas relacionadas con la autenticación, los usuarios y los posts. Además, configura el middleware CORS para permitir las solicitudes desde cualquier origen. Define un endpoint raíz que devuelva un mensaje de bienvenida. Y finalmente, inicia el servidor de desarrollo con Uvicorn en el puerto 8000.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, users, posts

app = FastAPI(title="TC01", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la TC01 de BD2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
