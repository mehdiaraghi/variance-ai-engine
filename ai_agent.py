import json

class AIReportGenerator:
    def __init__(self,report_payload:dict):
        self.report_payload = report_payload



    def needs_ai_analysis(self)-> bool:
        return len(self.report_payload["critical_cost_centers"])>0

        

    def build_llm_prompt(self) -> dict:
        if self.needs_ai_analysis():
             critical_json_str = json.dumps(self.report_payload["critical_cost_centers"], indent=2)
             total_var = self.report_payload["total_revenue_variance"]
             user_prompt_text = f"Total Revenue Variance: {total_var}\nCritical Cost Centers:\n{critical_json_str}"
             llm_prompt = {
                 "call_llm":True,
                 "system_prompt" : "You're a senior FP&A, you're given the information regarding cost center that are flagged as critical. do not hallucinate and do not make up numbers, based on the given analyze the critical center",
                 "user_prompt": user_prompt_text
                 }
             return llm_prompt
        else:
            return {"call_llm": False, "message": "All cost centers are on track. No AI analysis required."} 


