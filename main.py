import secrets, string
from fastapi import FastAPI, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from security import api_key_auth

app = FastAPI(title="Password Generator", description="A simple API for generating passwords. You can specify the length, and if it would contain lowercases, uppercases, special characters and or digits.")

class GeneratedPassword(BaseModel):
    newpass: str

@app.get("/newpass/", tags=["Generator"], response_model=GeneratedPassword, status_code=200, dependencies=[Depends(api_key_auth)])
async def generate_password( length: int = 8, uppercases: bool = True, lowercases: bool = True, digits: bool = True, specials: bool = False) -> dict:
    alphabet = []
    if uppercases:
        alphabet.extend( string.ascii_uppercase)
    if lowercases:
        alphabet.extend( string.ascii_lowercase)
    if digits:
        alphabet.extend( string.digits)
    if specials:
        alphabet.extend( string.punctuation)
    if not alphabet:
        alphabet = string.ascii_lowercase
    password = ''.join(secrets.choice(alphabet) for _ in range( length))
    return {"newpass": password}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=exc.errors()[0],
    )