from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient as InfluxDBClientV1
import pandas as pd
import json
import time

# MQTT info
broker = "37.156.47.96"  # MQTT broker address
port = 30511  # MQTT port
topic = "telemetry/"  # Topic where data will be published

# Digital twin info
namespace = "example"
pv_system_name = "franklin"

START_TS = (datetime.now() - timedelta(hours=2)).replace(minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')
END_TS = (datetime.now() - timedelta(hours=1)).replace(minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')

# Match and gap Influx -> Ditto
matchandgap_query = {
     'VM_MPPT246':       "SELECT mean(""Vm"") FROM ""data"" WHERE (""source"" = 'mppt_importer_BIPVdSHADE' AND ""mpptid"" = '246') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'VM_MPPT286':       "SELECT mean(""Vm"") FROM ""data"" WHERE (""source"" = 'mppt_importer_BIPVdSHADE' AND ""mpptid"" = '286') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'VM_MPPT287':       "SELECT mean(""Vm"") FROM ""data"" WHERE (""source"" = 'mppt_importer_BIPVdSHADE' AND ""mpptid"" = '287') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'IM_MPPT246':       "SELECT mean(""Im"") FROM ""data"" WHERE (""source"" = 'mppt_importer_BIPVdSHADE' AND ""mpptid"" = '246') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'IM_MPPT286':       "SELECT mean(""Im"") FROM ""data"" WHERE (""source"" = 'mppt_importer_BIPVdSHADE' AND ""mpptid"" = '286') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'IM_MPPT287':       "SELECT mean(""Im"") FROM ""data"" WHERE (""source"" = 'mppt_importer_BIPVdSHADE' AND ""mpptid"" = '287') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'PYR1':             "SELECT mean(\"6_5\")  / 0.0000539 FROM ""data"" WHERE time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'PYR2':             "SELECT mean(\"6_6\")  / 0.0000512 FROM ""data"" WHERE time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'PYR3':             "SELECT mean(\"6_7\")  / 0.0000491 FROM ""data"" WHERE time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBD_L2_LEFT_1':    "SELECT mean(\"1_1\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBD_L2_RIGHT_1':   "SELECT mean(\"1_2\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBOM_L2_LEFT_2':   "SELECT mean(\"1_3\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBOM_L2_RIGHT_2':  "SELECT mean(\"1_4\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TAIR_L2_LEFT_3':   "SELECT mean(\"2_1\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TAIR_L2_RIGHT_3':  "SELECT mean(\"2_2\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBD_L5_LEFT_1':    "SELECT mean(\"2_3\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBOM_L5_LEFT_2':   "SELECT mean(\"2_4\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TBOM_L5_RIGHT_2':  "SELECT mean(\"3_1\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TAIR_L5_LEFT_3':   "SELECT mean(\"3_2\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'TAIR_L5_RIGHT_3':  "SELECT mean(\"3_3\") FROM ""data"" WHERE (""source"" = 'datexel_importer_BIPVdSHADE') AND time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'GHI_GP':           "SELECT mean(""Raw_GlobalHor_Irr"") / 0.009004 FROM ""meteo"" WHERE time >= '"+START_TS+"' AND time < '"+END_TS+"'",
     'DHI_GP':           "SELECT mean(""Raw_Diff_Irr"") / 0.008841 FROM ""meteo"" WHERE time >= '"+START_TS+"' AND time < '"+END_TS+"'"
}

matchandgap_things = {
     'VM_MPPT246':       "MPPT246",
     'VM_MPPT286':       "MPPT286",
     'VM_MPPT287':       "MPPT287",
     'IM_MPPT246':       "MPPT246",
     'IM_MPPT286':       "MPPT286",
     'IM_MPPT287':       "MPPT287",
     'PYR1':             "Pyr1",
     'PYR2':             "Pyr2",
     'PYR3':             "Pyr3",
     'TBD_L2_LEFT_1':    "L2_left_1",
     'TBD_L2_RIGHT_1':   "L2_right_1",
     'TBOM_L2_LEFT_2':   "L2_left_2",
     'TBOM_L2_RIGHT_2':  "L2_right_2",
     'TAIR_L2_LEFT_3':   "L2_left_3",
     'TAIR_L2_RIGHT_3':  "L2_right_3",
     'TBD_L5_LEFT_1':    "L5_left_1",
     'TBOM_L5_LEFT_2':   "L5_left_2",
     'TBOM_L5_RIGHT_2':  "L5_right_2",
     'TAIR_L5_LEFT_3':   "L5_left_3",
     'TAIR_L5_RIGHT_3':  "L5_right_3",
     'GHI_GP':           "GlobalPyranometer1",
     'DHI_GP':           "GlobalPyranometer1"
}

matchandgap_things_types = {
     "MPPT246":             "MPPT",
     "MPPT286":             "MPPT",
     "MPPT287":             "MPPT",
     "Pyr1":                "PYR",
     "Pyr2":                "PYR",
     "Pyr3":                "PYR",
     "L2_left_1":           "CELL",
     "L2_right_1":          "CELL",
     "L2_left_2":           "CELL",
     "L2_right_2":          "CELL",
     "L2_left_3":           "CELL",
     "L2_right_3":          "CELL",
     "L5_left_1":           "CELL",
     "L5_left_2":           "CELL",
     "L5_right_2":          "CELL",
     "L5_left_3":           "CELL",
     "L5_right_3":          "CELL",
     "GlobalPyranometer1":  "GlobalPyranometer"
}

matchandgap_attributes = {
     'VM_MPPT246':       "Vm",
     'VM_MPPT286':       "Vm",
     'VM_MPPT287':       "Vm",
     'IM_MPPT246':       "Im",
     'IM_MPPT286':       "Im",
     'IM_MPPT287':       "Im",
     'PYR1':             "Irradiance",
     'PYR2':             "Irradiance",
     'PYR3':             "Irradiance",
     'TBD_L2_LEFT_1':    "Tbd",
     'TBD_L2_RIGHT_1':   "Tbd",
     'TBOM_L2_LEFT_2':   "Tbom",
     'TBOM_L2_RIGHT_2':  "Tbom",
     'TAIR_L2_LEFT_3':   "Tair",
     'TAIR_L2_RIGHT_3':  "Tair",
     'TBD_L5_LEFT_1':    "Tbd",
     'TBOM_L5_LEFT_2':   "Tbom",
     'TBOM_L5_RIGHT_2':  "Tbom",
     'TAIR_L5_LEFT_3':   "Tair",
     'TAIR_L5_RIGHT_3':  "Tair",
     'GHI_GP':           "GHI",
     'DHI_GP':           "DHI"
}

# MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection")
    else:
        print(f"Connection failed with code {rc}")

def get_ditto_protocol_msg(name, value):
    return {
        "topic": "{}/{}/things/twin/commands/merge".format(namespace, name),
        "headers": {
            "content-type": "application/merge-patch+json"
        },
        "path": "/features",
        "value": value
    }

def get_ditto_protocol_msg_cell(name, value):
    return '{\"topic\": \"'+namespace+'/'+name+'/things/twin/commands/merge\"'.format(namespace, name) + ',\"headers\": {\"content-type\": \"application/merge-patch+json\"},\"path\": \"/features\",\"value\":'+value+'}'

def get_ditto_protocol_value_mppt(ts, vm, im):
    return {
        "Vm": {
            "properties": {
                "value": vm,
                "time": ts
            }
        },
        "Im": {
            "properties": {
                "value": im,
                "time": ts
            }
        }
    }

def get_ditto_protocol_value_pyr(ts, irradiance):
    return {
        "Irradiance": {
            "properties": {
                "value": irradiance,
                "time": ts
            }
        }
    }

def get_ditto_protocol_value_global_pyr(ts, ghi, dhi):
    return {
        "GHI": {
            "properties": {
                "value": ghi,
                "time": ts
            }
        },
        "DHI": {
            "properties": {
                "value": dhi,
                "time": ts
            }
        }
    }

def get_ditto_protocol_value_cell(ts, tbd, tbom, tair):
     json_val = '{'
     if tbd is not None:
          json_val = json_val + '\"Tbd\": {\"properties\": {\"value\": ' + str(tbd) + ',\"time\": ' + str(ts) + '}}'
     if tbom is not None:
          if json_val == '{':
               json_val = json_val + '"Tbom": {"properties": {"value": ' + str(tbom) + ',"time": ' + str(ts) + '}}'
          else:
               json_val = json_val + ',"Tbom": {"properties": {"value": ' + str(tbom) + ',"time": ' + str(ts)  + '}}'
     if tair is not None:
          if json_val == '{':
               json_val = json_val + '"Tair": {"properties": {"value": ' + str(tair) + ',"time": ' + str(ts)  + '}}'
          else:
               json_val = json_val + ',"Tair": {"properties": {"value": ' + str(tair) + ',"time": ' + str(ts)  + '}}'
     json_val = json_val + '}'
     return json_val

influx_client = InfluxDBClientV1('199.247.12.243', 8086, 'admin', 'pTno2eHTxLmW*', 'franklinmockup')

#Things classification
mppt_df = pd.DataFrame(columns=['thing','Vm', 'Im'])
pyr_df = pd.DataFrame(columns=['thing', 'Irradiance'])
cell_df = pd.DataFrame(columns=['thing', 'Tbom', 'Tbd', 'Tair'])
g_pyr_df = pd.DataFrame(columns=['thing', 'GHI', 'DHI'])

for thing in matchandgap_things_types.keys():

     if matchandgap_things_types.get(thing) == "MPPT":
          mppt_df.loc[len(mppt_df)] = [thing, None, None]
     if matchandgap_things_types.get(thing) == "PYR":
          pyr_df.loc[len(pyr_df)] = [thing, None]
     if matchandgap_things_types.get(thing) == "CELL":
          cell_df.loc[len(cell_df)] = [thing, None, None, None]
     if matchandgap_things_types.get(thing) == "GlobalPyranometer":
          g_pyr_df.loc[len(g_pyr_df)] = [thing, None, None]

#Extracting data from InfluxDB
for measure in matchandgap_query.keys():

     query = matchandgap_query.get(measure)
     result_influx = influx_client.query(query)
     series_influx = list(result_influx.get_points())
     if len(series_influx)>0:
         series_influx[0]['time'] = (datetime.strptime(series_influx[0]['time'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
         ditto_thing = matchandgap_things.get(measure)

         if ditto_thing in mppt_df['thing'].values:
              mppt_df.loc[mppt_df.thing == ditto_thing, matchandgap_attributes.get(measure)] = series_influx[0]['mean']
         if ditto_thing in pyr_df['thing'].values:
              pyr_df.loc[pyr_df.thing == ditto_thing, matchandgap_attributes.get(measure)] = series_influx[0]['mean']
         if ditto_thing in cell_df['thing'].values:
              cell_df.loc[cell_df.thing == ditto_thing, matchandgap_attributes.get(measure)] = series_influx[0]['mean']
         if ditto_thing in g_pyr_df['thing'].values:
             g_pyr_df.loc[g_pyr_df.thing == ditto_thing, matchandgap_attributes.get(measure)] = series_influx[0]['mean']

#Sending data via MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(broker, port, 60)

timestamp_obj = datetime.strptime(END_TS, "%Y-%m-%d %H:%M:%S")
epoch_time = int(timestamp_obj.timestamp())*1000

for index, mppt in mppt_df.iterrows():
    if mppt['Vm'] is not None or  mppt['Im'] is not None:
        msg = get_ditto_protocol_msg(mppt['thing'], get_ditto_protocol_value_mppt(epoch_time, mppt['Vm'], mppt['Im']))
        client.publish(topic + namespace + "/"  +mppt['thing'], json.dumps(msg))

for index, pyr in pyr_df.iterrows():
    if pyr['Irradiance'] is not None:
        msg = get_ditto_protocol_msg(pyr['thing'], get_ditto_protocol_value_pyr(epoch_time, pyr['Irradiance']))
        client.publish(topic + namespace + "/" + pyr['thing'], json.dumps(msg))

for index, cell in cell_df.iterrows():
    if cell['Tbd'] is not None or cell['Tbom'] is not None or cell['Tair'] is not None:
        msg = get_ditto_protocol_msg_cell(cell['thing'], get_ditto_protocol_value_cell(epoch_time, cell['Tbd'], cell['Tbom'], cell['Tair']))
        client.publish(topic + namespace + "/" + cell['thing'], str(msg))

for index, gpyr in g_pyr_df.iterrows():
    if gpyr['GHI'] is not None or  gpyr['DHI'] is not None:
        msg = get_ditto_protocol_msg(gpyr['thing'], get_ditto_protocol_value_global_pyr(epoch_time, gpyr['GHI'], gpyr['DHI']))
        client.publish(topic + namespace + "/"  +gpyr['thing'], json.dumps(msg))

print("Data published via MQTT")

client.disconnect()