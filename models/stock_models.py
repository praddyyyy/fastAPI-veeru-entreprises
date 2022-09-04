from pydantic import BaseModel
from typing import Dict, List

class Stock(BaseModel):
    model: str
    description: str
    price: str
