import esp_send_func
import mq5
import machine
import utime
import network


max_failed = 10
sleep_sec = 6
failed_connections = 0

sta_if = network.WLAN(network.STA_IF)

while not sta_if.isconnected():
    if failed_connections > max_failed:
        machine.reset()
    else:
        failed_connections = failed_connections + 1
    utime.sleep(10)


def start():
    try:
        print("Starting esp_mq5")
        failed_attempts = 0
        while True:
            data = mq5.modulmq5()
            if data:
                resp = esp_send_func.send_to_ovh_metrics(sensor_name="esp_mq5",value=data)
                if not resp:
                    if failed_attempts > max_failed:
                        machine.reset()
                    else:
                        failed_attempts = failed_attempts + 1
            utime.sleep(sleep_sec)
    except Exception as e:
        print("Start failed due to exception: {}".format(e))
        print("Reloading ESP!")
        machine.reset()
