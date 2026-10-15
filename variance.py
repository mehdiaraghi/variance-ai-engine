class Variance:
    def __init__(self,cost_center:str,time_period:str,
                 revenue_actual: float , revenue_forecast:float, 
                 volume_actual:int, volume_forecast:int)-> None:
        self.cost_center = cost_center
        self.time_period = time_period.upper()
        if self.time_period not in ["PTD","YTD"]:
            raise ValueError ("Time Period should be either PTD or YTD")
        self.revenue_actual = revenue_actual
        self.revenue_forecast = revenue_forecast
        self.volume_actual = volume_actual
        self.volume_forecast = volume_forecast

        if self.revenue_forecast <=0 or self.volume_forecast<=0:
            raise ValueError ("Forecasts Values for Revenue and Volume should be Greater than 0")

    def __repr__(self) -> str:
        return f"Variance(cost_center = '{self.cost_center}',time_period = '{self.time_period}', status = {self.flag_status()})"
        

    def absolute_variance(self) -> float:
        revenue_variance = round(self.revenue_actual - self.revenue_forecast,ndigits =2)
        return revenue_variance

    def percent_variance(self)-> float:
        percent_variance = round(self.absolute_variance()/ self.revenue_forecast*100,ndigits=2)
        return percent_variance

    def flag_status(self)-> str:
        revenue_percent = self.percent_variance()
        if  revenue_percent >= 0 :
            revenue_status = "Good Status"
        elif -5 < revenue_percent < 0  :
            revenue_status = "Attention"
        else:
            revenue_status = "Critical Situation"

        return revenue_status

    def dict_record(self)-> dict:
       return {'cost_center':self.cost_center,
        'time_period': self.time_period,
        'revenue_actual' : self.revenue_actual,
        'revenue_forecast' : self.revenue_forecast,
        'volume_actual' : self.volume_actual,
        'volume_forecast' : self.volume_forecast,
        'revenue_variance': self.absolute_variance(),
        'revenue_percent': self.percent_variance(),
        'revenue_status': self.flag_status()}

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






var1 = [{'cost_center': 'CC-101', 'time_period': 'PTD', 'revenue_actual': 10000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-102', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-103', 'time_period': 'PTd', 'revenue_actual': 9000, 'revenue_forecast': 9500, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-104', 'time_period': 'qtD', 'revenue_actual': 10000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-105', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 0},
        {'cost_center': 'CC-106', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9000, 'volume_actual': 5000}]

test1 = VarianceProcessor(var1)        
print(test1.valid_records)
print(test1.fail_records)
print(test1.process_result())
print(test1.critical_situation())
print(test1.total_variance())
print(test1.generate_report_payload())