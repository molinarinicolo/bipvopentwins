from pydantic import BaseModel

class PowerRequest(BaseModel):
    startTS: str
    endTS: str
