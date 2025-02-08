import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api import api
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper


class Query(BaseModel):
    inquiry: str
    chat_history: str

cdp= CdpAgentkitWrapper()
toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)
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
    toolkit.get_tools()[13].invoke(input={"asset_id": "eth"})
    return api.generate_response(query.inquiry, query.chat_history)

@app.get("/chat")
def chat():
    return "Hello World!"
