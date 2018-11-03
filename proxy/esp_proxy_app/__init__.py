from flask import Flask, request, jsonify, Response
from influxdb import InfluxDBClient

import logging
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'sensordb')
app = Flask(__name__)
log = app.logger
log.setLevel(logging.DEBUG)

allowed_sensors = dict(
    token_mq135="esp_mq135",
    token_mq5="esp_mq5",
    token_mp503="esp_mp503",
    token_tsl2581fn="esp_tsl2581fn",
    token_dfrobot="esp_dfrobot",
    token_ds18b20="esp_ds18b20",
    token_hcsr501="esp_hcsr501"
)


@app.route('/write', methods=['POST'])
def proxy_post():
    sensor_token = request.headers.get("sensor_token", None)
    data = request.get_json()
    log.debug("sensor_token {}".format(sensor_token))
    log.debug("json data {}".format(data))
    log.debug("post data {}".format(request.get_data()))

    if type(data) is not dict:
        response = jsonify(error="Data structure is incorrect")
        response.status_code = 400
        return response

    if sensor_token not in allowed_sensors:
        response = jsonify(error="Sensor is not allowed")
        response.status_code = 401
        return response

    if "data_type" not in data:
        response = jsonify(error="Data not correct, 'data_type' is missing")
        response.status_code = 400
        return response

    if "value" not in data:
        response = jsonify(error="Data not correct, 'value' is missing")
        response.status_code = 400
        return response

    try:
        sensor_data = [
            {
                "time": datetime.now(),
                "measurement": "temperature",
                "fields": {
                    "value": data.get("value")
                }
            }
        ]
        log.debug("labeled_data {}".format(sensor_data))
        client.write(sensor_data)
    except Exception as exception:
        log.debug("Could not send data, exception {}".format(exception))
        return Response(response="Could not send data", status=500)

    return jsonify({"data": str(sensor_data)})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=443)
