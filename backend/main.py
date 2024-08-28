from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp_handler import NLPHandler

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp_handler = NLPHandler()

class Query(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart Reporting Tool API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query")
async def process_query(query: Query):
    try:
        response = nlp_handler.process_query(query.text)
        return {"result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
