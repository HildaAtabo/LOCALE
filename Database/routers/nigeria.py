from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Nigeria,Regions, States
from database import engine, SessionLocal
from starlette import status
from .auth import get_current_developer


nigeria_router = APIRouter()

models.Base.metadata.create_all(bind=engine)
 
def get_nigeria_db():
    nigeria_db = SessionLocal()
    try:
        yield nigeria_db
    finally:
        nigeria_db.close()

nigeria_db_dependency = Annotated[Session, Depends(get_nigeria_db)]

class NigeriaRequest(BaseModel):
    region: str = Field(min_length=3)
    state: str = Field(min_length=3, max_length=100)

class RegionRequest(BaseModel):
    name: str = Field(min_length=3)
    state: str = Field(min_length=3, max_length=100)


class StateRequest(BaseModel):
    name: str = Field(min_length=3)
    lga: str = Field(min_length=3, max_length=100)
    

@nigeria_router.get("/")
async def read_all(nigeria_db: nigeria_db_dependency):
    search_Nigeria =  nigeria_db.query(Nigeria).all()
    return search_Nigeria

@nigeria_router.get("/region/{region_id}", status_code=status.HTTP_200_OK) 
async def read_one(nigeria_db: nigeria_db_dependency, region_id: int = Path(gt=0)):
    region_model = nigeria_db.query(Regions).filter(Regions.id == region_id).first()
    if region_model is not None:
        return region_model
    raise HTTPException(status_code=404, detail="Region not found")

#Create a region
@nigeria_router.post("/region", status_code=status.HTTP_201_CREATED)
async def create_region(nigeria_db: nigeria_db_dependency, region_request: RegionRequest):

    region_model = Regions(**region_request.model_dump())
    print(region_model)

    nigeria_db.add(region_model)
    nigeria_db.commit() 
    nigeria_db.refresh(region_model)

    return region_model


#Update a region
@nigeria_router.put("/region/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_region(nigeria_db: nigeria_db_dependency, 
                      region_id: int,
                      region_request: RegionRequest):
    region_model = nigeria_db.query(Regions).filter(Regions.id == region_id).first()
    if region_model is None:
        raise HTTPException(status_code=404, detail="Region not found")
    
    region_model.state = region_request.state

    nigeria_db.add(region_model)
    nigeria_db.commit()


#Delete a region
@nigeria_router.delete("/region/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(nigeria_db: nigeria_db_dependency, region_id: int = Path(gt=0)):
    region_model = nigeria_db.query(Regions).filter(Regions.id == region_id).first()
    if region_model is None:
        raise HTTPException(status_code=404, detail="Region not found")
        
    nigeria_db.delete(region_model)
    nigeria_db.commit()




@nigeria_router.get("/state/{state_id}", status_code=status.HTTP_200_OK) 
async def read_one(nigeria_db: nigeria_db_dependency, state_id: int = Path(gt=0)):
    state_model = nigeria_db.query(States).filter(States.id == state_id).first()
    if state_model is not None:
        return state_model
    raise HTTPException(status_code=404, detail="State not found")

#Create a state
@nigeria_router.post("/state", status_code=status.HTTP_201_CREATED)
async def create_state(nigeria_db: nigeria_db_dependency, state_request: StateRequest):

    state_model = States(**state_request.model_dump())
    nigeria_db.add(state_model)
    nigeria_db.commit()
    nigeria_db.refresh(state_model)

    return state_model

   
#Update a state
@nigeria_router.put("/state/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_state(nigeria_db: nigeria_db_dependency, 
                      state_id: int,
                      state_request: StateRequest):
    state_model = nigeria_db.query(States).filter(States.id == state_id).first()
    if state_model is None:
        raise HTTPException(status_code=404, detail="State not found")
    
    state_model.lga = state_request.lga

    nigeria_db.add(state_model)
    nigeria_db.commit()
   

#Delete a state
@nigeria_router.delete("/state/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_state(nigeria_db: nigeria_db_dependency, state_id: int = Path(gt=0)):
    state_model = nigeria_db.query(States).filter(States.id == state_id).first()
    if state_model is None:
        raise HTTPException(status_code=404, detail="State not found")
        
    nigeria_db.delete(state_model)
    nigeria_db.commit()