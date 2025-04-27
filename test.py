import json
import os
import sys
from evidently import Report
from evidently.presets import DataDriftPreset
from pandas import DataFrame
import pandas as pd

test_data = pd.read_csv(r"C:\Users\Prashant kumar singh\Desktop\US_Visa_verification\artifact\US_VISA\data_ingestion\2025-04-26-01-18-19\SPLITED\Test.csv")
train_data = pd.read_csv(r"C:\Users\Prashant kumar singh\Desktop\US_Visa_verification\artifact\US_VISA\data_ingestion\2025-04-26-01-18-19\SPLITED\Train.csv")

report = Report([DataDriftPreset()])
my_evl=report.run(train_data, test_data)

result = my_evl.json()
json_report = json.loads(result)
n_feature = []
metrics = json_report["metrics"]
for i in metrics:
    col =i["metric_id"].split("column=")[-1].split(")")[0]
    n_feature.append(col)

len(n_feature)

n_drifted_feature=metrics[0]['value']['count']

drift_status=metrics[0]['value']['share']
drift_status

print(len(n_feature[1:]))
print(f" No of n_drifted_feature :{n_drifted_feature}")
print(f" drift status: {drift_status}")