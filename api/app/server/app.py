import os
import glob

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from app.server.routes.chatbot.chatbot import router as Chat



app = FastAPI()


'''Deleting upload and generated filed for project documention POC'''
@app.on_event("shutdown")
def shutdown_event():
    files = glob.glob('app/server/routes/project_documentation/uploads/*')
    for f in files:
        os.remove(f)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to UPS Gen AI POC's!"}


# Adding origins and middleware to prevent CORS error
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)


# Creating endpoints
app.include_router(Chat, tags=["Chat"], prefix="/apis/chat")
