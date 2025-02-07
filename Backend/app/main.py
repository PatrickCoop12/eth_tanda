import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api import api


class Query(BaseModel):
    inquiry: str
    chat_history: str


# Create app and adding middleware (as good practice)
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat_response")
def chat_with_agent(query:Query):
    return api.generate_response(query.inquiry, query.chat_history)

@app.get("/chat")
def chat():
    return "Hello World!"
