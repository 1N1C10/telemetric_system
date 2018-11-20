from flask import Flask, request, jsonify, Response
from influxdb import InfluxDBClient

import logging

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'sensordb')
app = Flask(__name__)
log = app.logger
log.setLevel(logging.DEBUG)

allowed_sensors = dict(
    token_mp503="esp_mp503",
    token_dht22="esp_dht22",
    token_dfrobot="esp_dfrobot",
    token_ds18b20="esp_ds18b20",
    token_light="esp_light",
)


@app.route('/write', methods=['POST'])
def proxy_post():
    sensor_token = request.headers.get("sensor_token")
    data = request.get_json()
    log.debug("sensor_token {}".format(sensor_token))
    log.debug("json data {}".format(data))
    log.debug("post data {}".format(request.get_data()))

    if type(data) is not dict:
        return Response(response="Wrong data type", status=400)

    if sensor_token not in allowed_sensors:
        return Response(response="Sensor is not allowed", status=401)

    if "data_type" not in data:
        return Response(response="Data received not correct, missing 'data_type'", status=400)

    if "value" not in data:
        return Response(response="Data received not correct, missing 'value'", status=400)

    try:
        sensor_data = [
            {
                "measurement": data['data_type'],
                "fields": {
                    "value": data['value']
                }
            }
        ]
        log.debug("labeled_data {}".format(sensor_data))
        client.write_points(sensor_data)
    except Exception as exception:
        log.error("Could not send data, exception {}".format(exception))
        return Response(response="Could not send data", status=500)

    return jsonify({"data": str(sensor_data)})


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True, host='0.0.0.0', port=443)
