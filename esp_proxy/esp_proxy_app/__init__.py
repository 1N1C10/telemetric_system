from flask import Flask, request, jsonify, Response
#from flask_api import status
import requests
import logging
from datetime import datetime
app = Flask(__name__)
log = app.logger
log.setLevel(logging.DEBUG)

allowed_tokens = dict(
    token123121="esp_dev_1",
    token123121_mq135="esp_mq135"
)

OVH_WRITE_TOKEN = "KcJb_cJ3ZQG3.x8auMerMF_5CcMp.DsbdcWIbSi6JM1fgP1FIbH2_moPeIRPh2bVuEE1k8SNQwhd0R5LRjNTwCh6fnSjjvMtP.ipYEk1r96EPZlI6uCvmjhSzKnXw7HJ"

@app.route('/write', methods=['POST'])
def proxy_post():
    sensor_token = request.headers.get("X-SENSOR-TOKEN", None)
    data = request.get_json()
    log.debug("sensor_token {}".format(sensor_token))
    log.debug("json data {}".format(data))
    log.debug("post data {}".format(request.get_data()))

    if type(data) is not dict:
        response = jsonify(error="Data structure is incorrect")
        response.status_code = 400
        return response

    if sensor_token not in allowed_tokens:
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
        labeled_data = "{timestamp}// {metric_name}{{{labels}}} {metric_value}".format(
            timestamp = int(round(datetime.now().timestamp() *1000000)),
            metric_name=allowed_tokens.get(sensor_token),
            labels="data_type={data_type}".format(data_type=data.get("data_type")),
            metric_value=data.get("value")

        )
        log.debug("labeled_data {}".format(labeled_data))
        response = requests.post("https://warp10.gra1.metrics.ovh.net/api/v0/update",
                             data=labeled_data,
                             headers={'X-Warp10-Token':OVH_WRITE_TOKEN})
        log.debug("response {} {}".format(response, response.__dict__))
    except Exception as exception:
        log.debug("Could not send data, exception {}".format(exception))
        return Response(response="Could not send data",status=500)

    return jsonify({"data":str(labeled_data)})


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True, host='0.0.0.0', port=443)