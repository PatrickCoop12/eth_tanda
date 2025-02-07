import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api




# Create app and adding middleware (as good practice)
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
def chat_with_agent(inquiry:str, chat_history:str):
    return api.generate_response(inquiry, chat_history)
