from pydantic import BaseModel


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


class CenterInsight(BaseModel):
    cost_center : str
    primary_driver : str
    explanation : str
    recommended_action :str

class AIReportSchema(BaseModel):
    portfoli_summary : str
    critical_insight : list[CenterInsight]