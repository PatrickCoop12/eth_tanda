import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Create field validator for incoming request


# Create app and adding middleware (as good practice)
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def agent_request(inputs: str):
