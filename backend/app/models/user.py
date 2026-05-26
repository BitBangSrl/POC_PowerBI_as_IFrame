from pydantic import BaseModel

class UserContext(BaseModel):
    username: str
    role: str