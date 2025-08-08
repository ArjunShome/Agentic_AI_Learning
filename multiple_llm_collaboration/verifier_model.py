from pydantic import BaseModel

class Evaluation(BaseModel):
    is_approved: bool
    feedback: str
