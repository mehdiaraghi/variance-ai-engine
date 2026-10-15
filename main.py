from processor import VarianceProcessor




var1 = [{'cost_center': 'CC-101', 'time_period': 'PTD', 'revenue_actual': 10000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-102', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-103', 'time_period': 'PTd', 'revenue_actual': 9000, 'revenue_forecast': 9500, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-104', 'time_period': 'qtD', 'revenue_actual': 10000, 'revenue_forecast': 9000, 'volume_actual': 5000, 'volume_forecast': 5200},
        {'cost_center': 'CC-105', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 7000, 'volume_actual': 5000, 'volume_forecast': 0},
        {'cost_center': 'CC-106', 'time_period': 'PTd', 'revenue_actual': 8000, 'revenue_forecast': 9100, 'volume_actual': 5000}]

test1 = VarianceProcessor(var1)        
print(test1.valid_records)
print(test1.fail_records)
print(test1.process_result())
print(test1.critical_situation())
print(test1.total_variance())
print(test1.generate_report_payload())
