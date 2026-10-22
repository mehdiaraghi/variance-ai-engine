from fastapi import FastAPI
from processor import VarianceProcessor
from ai_agent import AIReportGenerator
import json

app = FastAPI()


@app.get("/health")
def check_system_health() -> dict:
    return {"status": "healthy", "message": "Mehdi's server is alive!"}


@app.post("/variance-report")
def variance_process(items : list[dict]) ->dict:
    processor = VarianceProcessor(items)
    payload = processor.generate_report_payload()
    ai_gen = AIReportGenerator(payload)
    payload["ai_agent_output"] = ai_gen.build_llm_prompt()
    with open ("latest_report.json", "w") as file:
        json.dump(payload,file,indent=2)
    
    return payload


