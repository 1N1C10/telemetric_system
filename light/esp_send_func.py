import urequests

config = {
    "esp_light": {
        "token": "token_light",
        "sensor_data_type": "lux",
    },
    "metrics_proxy": {
        "address": "https://192.168.43.9/write",
        "port": 443
    }
}


def send_to_proxy(sensor_name, value, data_type=None):
    if not data_type:
        data_type = config[sensor_name]["sensor_data_type"]
    response = urequests.post(
        config["metrics_proxy"]["address"],
        json={"data_type": data_type, "value": value},
        headers={"Content-Type": "application/json", "sensor_token": config[sensor_name]["token"]}
    )
    print(response.__dict__)
    return response
