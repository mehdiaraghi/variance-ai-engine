class VarianceProcessor:
    def __init__(self,data:list[dict]) -> None:
        self.data = data

    def len_data (self) -> int:
        return len(self.data)

    def variance (self) -> tuple:
        row_count = 0
        sucess_row = 0
        failed_row = 0
        valid_list = []
        error_list = []
        critical_list= []
        for record in self.data :
            try:
                time_period = record["time_period"].upper()
                if time_period not in ["PTD","YTD"]:
                    raise ValueError ("Time Period should be either PTD or YTD")

                revenue_actual = record["revenue_actual"]
                revenue_forecast = record["revenue_forecast"]
                volume_forecast = record["volume_forecast"]         
                if revenue_forecast <=0 or volume_forecast<=0:
                    raise ValueError ("Forecasts Values for Revenue and Volume should be Greater than 0")

                variance_absolute = round(revenue_actual - revenue_forecast , ndigits=2)
                variance_percent = round(variance_absolute/revenue_forecast*100, ndigits=2)
                record["variance_percent"] = variance_percent

                if variance_absolute >= 0:
                    record["status"] = "Good"
                elif -5.0<variance_absolute<0.0:
                    record["status"] = "Attention"
                else:
                    record["status"] = "Critical"
                    critical_list.append(record)

                
                
                valid_list.append(record)

                sucess_row +=1
            except ValueError as e:
                error_list.append(f"error successfully caught: record:{row_count} , {e}")
                failed_row +=1

            row_count +=1
        return valid_list, sucess_row,failed_row,error_list,critical_list

    def process_result(self) -> str:
        total_success = self.variance()[1]
        total_fail = self.variance()[2]
        error_list = self.variance()[3]

        return total_success,total_fail,error_list

    def critical_situation(self) -> list[dict]:
        return self.variance()[-1]

    def total_variance (self) -> float:
        valid_list_variance = self.variance()[0]
        revenue_total_variance = 0
        for valid in valid_list_variance:
            revenue_total_variance += valid["variance_percent"]

        revenue_total_variance_percent = round(revenue_total_variance/self.len_data(),2)

        return revenue_total_variance_percent
            

        
var1 = [{'cost_center': 'abcd', 'time_period': 'PTD', 'revenue_actual': 10000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'abcd', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'abcd', 'time_period': 'PTd', 'revenue_actual': 9000, 'revenue_forecast': 9500, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'abcd', 'time_period': 'qtD', 'revenue_actual': 10000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'abcd', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 0}]
        
print(VarianceProcessor(var1).len_data())
print(VarianceProcessor(var1).variance())
print(VarianceProcessor(var1).process_result())
print(VarianceProcessor(var1).critical_situation())
print(VarianceProcessor(var1).total_variance())