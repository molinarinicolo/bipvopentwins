from fastapi import FastAPI, HTTPException
import pickle
from .schemas import PowerRequest
from influxdb import InfluxDBClient
import pandas as pd
import datetime
import sklearn
import joblib
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

model_path = dir_path + '/ols_model.pkl'

app = FastAPI()

model = joblib.load(model_path)

feature_names = ['GHI', 'DHI', 'Month', 'Day', 'Time_factor']

@app.post("/get_power")
def get_occupancy_sample(data: PowerRequest):
    try:

        data_dict = data.model_dump()
        influx_client = InfluxDBClient('199.247.12.243', 8086, 'admin', 'pTno2eHTxLmW*', 'franklinmockup')

        start_ts = str((datetime.datetime.strptime(data_dict['startTS'], '%Y-%m-%d %H:%M:%S')))
        end_ts = str((datetime.datetime.strptime(data_dict['endTS'], '%Y-%m-%d %H:%M:%S')))

        result_opt = influx_client.query("SELECT mean(""Raw_GlobalHor_Irr"") / 0.009004 as GHI, mean(""Raw_Diff_Irr"")  / 0.008841 as DHI FROM ""meteo"" WHERE time >= '"+start_ts+"' AND time < '"+end_ts+"' GROUP BY time(1m)")

        series_opt = list(result_opt.get_points())

        model_input = [
            [
                float(sample['GHI']),
                float(sample['DHI']),
                int(datetime.datetime.strptime(sample['time'], '%Y-%m-%dT%H:%M:%SZ').month),
                int(datetime.datetime.strptime(sample['time'], '%Y-%m-%dT%H:%M:%SZ').day),
                float(datetime.datetime.strptime(sample['time'], '%Y-%m-%dT%H:%M:%SZ').hour + datetime.datetime.strptime(
                    sample['time'], '%Y-%m-%dT%H:%M:%SZ').minute / 60),
            ]
            for sample in series_opt
        ]

        prediction = model.predict(model_input)

        model_output = [
            [
                sample['time'],
                prediction[x]
            ]
            for x, sample in enumerate(series_opt)
        ]

        return {'Power': model_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

@app.get("/version")
def version():

    return {"version": "1.0"}

@app.get("/healthz")
def healthz():
    """
    Kubernetes uses this endpoint to check if our app is alive.
    If this returns a 200 OK, the pod is considered healthy.
    """
    return {"ok": True}

def test_truth():
    assert 1 == 1

