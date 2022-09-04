from operator import mod
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBearer
from .utils import VerifyToken
from models.stock_models import Stock, Model
from config.db import collection
from schemas.stock_schemas import stocksEntity

token_auth_scheme = HTTPBearer()
user = APIRouter()

@user.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! "
                "You don't need to be authenticated to see this.")
    }
    return result


@user.get("/api/private")
def private(response: Response, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""

    # We need to protect this endpoint!
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    result_msg = {
        "status": "success",
        "msg": ("Hello from a private endpoint! "
                "You need to be authenticated to see this.")
    }
    return result_msg

@user.post('/create-stock')
async def create_user(stock: Stock):
    _id = collection.insert_one(dict(stock))
    stock = stocksEntity(collection.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data": stock}

@user.get('/find-stock-model')
async def get_user(model: Model):
    stock = stocksEntity(collection.find({"model": model.model}))
    return {"status": "ok", "data": stock}