from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp_handler import NLPHandler
from chart_generator import ChartGenerator
from csv_reader import CSVReader

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

csv_reader = CSVReader("mock_sales_data.csv")
csv_reader.read_file()
nlp_handler = NLPHandler()
chart_generator = ChartGenerator(csv_reader.get_data())

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
        chart_data = response['chart_data']
        sales_table = chart_generator.generate_sales_table(response.get('product'), response.get('time_period'))
        return {
            "result": response['result'],
            "chart_type": response['chart_type'],
            "chart_data": chart_data,
            "sales_table": sales_table
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
