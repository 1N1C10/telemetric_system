
import urequests

ovh_config = {
    "sensors": {
        "esp_mp503":{
            "token":"token123121_mp503",
            "default_data_type":"air_quality"
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

"""
if __name__ == "__main__":
    import random
    send_to_ovh_metrics("esp_dev_1", random.randrange(999))
"""