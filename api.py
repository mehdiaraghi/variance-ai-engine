from fastapi import FastAPI
from processor import VarianceProcessor


app = FastAPI()


@app.get("/health")
def check_system_health() -> dict:
    return {"status": "healthy", "message": "Mehdi's server is alive!"}

@app.post("/sum-numbers")
def calculate_sum(items: list[int]) -> dict:
    total = sum(items)
    return {"total_sum": total}

@app.post("/variance-report")
def variance_process(items : list[dict]) ->dict:
    obj = VarianceProcessor(items)
    return obj.generate_report_payload()
