from fastapi import FastAPI
from Interact_api import interact_router
from Extract_api import extract_router

app = FastAPI()

app.include_router(interact_router)
app.include_router(extract_router)
