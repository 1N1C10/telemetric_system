import urequests

ovh_config = {
    "sensors": {
        "esp_mq135":{
            "token":"token123121_mq135",
            "default_data_type":"temperature"
        }
    },
    "metrics_proxy": {
        "address":"https://192.168.43.9/write",
        "port":443
    }
}


def send_to_ovh_metrics(sensor_name, value, data_type=None):

    if not data_type:
        data_type = ovh_config["sensors"][sensor_name]["default_data_type"]
    response = urequests.post(
        ovh_config["metrics_proxy"]["address"],
        json={"data_type":data_type, "value":value},
        headers={"Content-Type":"application/json","X-SENSOR-TOKEN":ovh_config["sensors"][sensor_name]["token"]}
    )
    print(response.__dict__)
    return response