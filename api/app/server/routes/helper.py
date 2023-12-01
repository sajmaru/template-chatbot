from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# definig format in which response will be sent to frontend
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

# Definig error messages 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

