from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Developers
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import timedelta, datetime


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "c03db7649e965227ca372f72506a7b05755276e7e6710fd172bfaf69f14589ca"
ALGORITHM = "HS256"
 


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")



class CreateDeveloperRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    role: str
    api_key: str

class Token(BaseModel):
    access_token: str
    token_type: str


def get_nigeria_db():
    nigeria_db = SessionLocal()
    try:
        yield nigeria_db
    finally:
        nigeria_db.close()
    
nigeria_db_dependency = Annotated[Session, Depends(get_nigeria_db)]

def authenticate_developer(username: str, password: str, nigeria_db):
    developer = nigeria_db.query(Developers).filter(Developers.username == username).first()
    if not developer:
        return False
    if not bcrypt_context.verify(password, developer.hashed_password):
        return False
    return developer

def create_access_token(username: str, developer_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': developer_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_developer(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        developer_id:  int = payload.get("id")
        if username is None or developer_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Invalid authentication credentials")
        return{"username": username, "id": developer_id} 
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Invalid authentication credentials")

# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_developer(nigeria_db: nigeria_db_dependency, create_developer_request: CreateDeveloperRequest):
    create_developer_model = Developers(
        email = create_developer_request.email,
        username = create_developer_request.username,
        first_name = create_developer_request.first_name,
        last_name = create_developer_request.last_name,
        role = create_developer_request.role,
        hashed_password = bcrypt_context.hash(create_developer_request.password),
        is_active = True,
        api_key = create_developer_request.api_key
    )
    
    nigeria_db.add(create_developer_model)
    nigeria_db.commit()

    
    return create_developer_model

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 nigeria_db: nigeria_db_dependency):
    developer = authenticate_developer(form_data.username, form_data.password, nigeria_db)

    if not developer:
        return "Failed Authentication"
    
    

    token = create_access_token(developer.username, developer.id, timedelta(minutes=15))
    
    return {
        "access_token": token,
        "token_type": "bearer"}


    

