# -------------------------------- IMPORTS -------------------------------
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, users, posts
from src.models.task import Task
# ------------------------------------------------------------------------
# Create a FastAPI instance
app = FastAPI(title="TC01", version="0.1.0")

# Agregar el middleware de CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de los diferentes endpoints
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

# -------------------------------- ROUTES --------------------------------
# GET request to the root of the application
@app.get("/")
async def root():
    return {"message": "Bienvenido a la TC01 de BD2"}

# POST request to create a new task
@app.post("/task")
async def create_task(task: Task):
    print(task)
    return task
# ------------------------------------------------------------------------

# Define a port and host to run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
