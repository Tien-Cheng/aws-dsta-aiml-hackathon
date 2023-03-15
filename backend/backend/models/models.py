from pydantic import BaseModel

# class PredictionResponse(BaseModel):
#     #TODO

class Text(BaseModel):
    text: str
