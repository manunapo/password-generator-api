import secrets, string
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

class Password(BaseModel):
    new_pass: str

@app.get("/password/", response_model=Password, status_code=200)
async def generate_password( length: int = 8, uppercases: bool = True, lowercases: bool = True, digits: bool = True, specials: bool = False):
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
    return {"new_pass": password}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=exc.errors()[0],
    )