import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from models import AIReportSchema

load_dotenv()



class AIReportGenerator:
    def __init__(self,report_payload:dict):
        self.report_payload = report_payload



    def needs_ai_analysis(self)-> bool:
        return len(self.report_payload["critical_cost_centers"])>0

        

    def build_llm_prompt(self) -> dict:
        if self.needs_ai_analysis():
            
            my_key = os.getenv("GEMINI_API_KEY")
            if my_key is None:
                raise ValueError ("API Key is missing! Check your .env file.")

            client = genai.Client(api_key=my_key)
            critical_json_str = json.dumps(self.report_payload["critical_cost_centers"], indent=2)
            total_var = self.report_payload["total_revenue_variance"]
            user_prompt_text = f"Total Revenue Variance: {total_var}\nCritical Cost Centers:\n{critical_json_str}"
            system_prompt_str = "You're a senior FP&A, you're given the information regarding cost center that are flagged as critical. do not hallucinate and do not make up numbers, based on the given analyze the critical center"
            response = client.models.generate_content(
                model= "gemini-3.8-flash",
                contents= user_prompt_text,
                config = types.GenerateContentConfig(
                    system_instruction= system_prompt_str,
                    temperature= 0.2,
                    response_mime_type="application/json",
                    response_schema= AIReportSchema
                ),
            )
            ai_answer = json.loads(response.text)
            return {"call_llm": True,
                    "ai_analysis" : ai_answer
                    }

        else:
            return {"call_llm": False, 
                    "message": "All cost centers are on track. No AI analysis required."} 


