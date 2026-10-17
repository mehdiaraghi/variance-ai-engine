from models import Variance
import json

class VarianceProcessor:
    def __init__(self,data:list[dict]) :
        self.data = data
        self.valid_records = []
        self.fail_records = []
        for record in self.data:
            try:
                obj = Variance(**record)
                self.valid_records.append(obj)
            
            except (ValueError, TypeError) as e:
                center_name = record.get('cost_center','UNKNOWN')
                self.fail_records.append({ "center": center_name, "error": str(e)})  


    def process_result(self) -> tuple:
        valid_records_counts = len(self.valid_records)
        fail_records_counts = len(self.fail_records)

        return valid_records_counts, fail_records_counts

    def critical_situation(self)-> list[dict]:
        critical_records = []
        for critical in self.valid_records:
            if critical.flag_status() == "Critical Situation":
                critical_records.append(critical.dict_record())

        return critical_records

    def total_variance(self) -> float:
        actual_total_variance = 0

        for var in self.valid_records:
            actual_total_variance += var.absolute_variance()

        return round(actual_total_variance, ndigits=2)


    def generate_report_payload(self)->dict:
        return{
            "total_input_records" : len(self.data),
            "valid_count" : len(self.valid_records),
            "failed_count" : len(self.fail_records),
            "total_revenue_variance" : self.total_variance(),
            "critical_cost_centers" : self.critical_situation(),
            "error_logs" : self.fail_records
        }    





