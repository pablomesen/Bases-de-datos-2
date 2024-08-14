from pydantic import BaseModel

# Basic Pydantic model
class Task(BaseModel):
    name: str
    description: str
    completed: bool
