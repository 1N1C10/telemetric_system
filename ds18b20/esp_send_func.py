import urequests

config = {
    "esp_ds18b20": {
        "token": "token_ds18b20",
        "sensor_data_type": "temperature",
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


"""
if __name__ == "__main__":
    import random
    send_to_ovh_metrics("esp_dev_1", random.randrange(999))
"""