from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent_tailor import run_agent_tailor, create_final_workspace

app = FastAPI()

# Allow your frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local hackathon testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TailorRequest(BaseModel):
    job_description: str
    data_pool: str

@app.post("/api/generate")
async def generate_documents(request: TailorRequest):
    print("Received request from Stitch UI!")

    result = run_agent_tailor(request.job_description, request.data_pool)

    if not result:
        raise HTTPException(status_code=500, detail="AI generation failed.")

    create_final_workspace(result, request.job_description)

    return {
        "status": "success", 
        "message": "Workspace created successfully!",
        "data": result
    }