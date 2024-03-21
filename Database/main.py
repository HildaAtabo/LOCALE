from fastapi import FastAPI
from routers.auth import router
from routers.nigeria import nigeria_router


app = FastAPI()

#Include the router

app.include_router(router)
app.include_router(nigeria_router)

