import esp_send_func
import mq135
import machine
import utime
import network

max_failed = 10
sleep_sec = 6
failed_connections = 0

sta_if = network.WLAN(network.STA_IF)

while not sta_if.isconnected():
    print("No internet, going to sleep")
    if failed_connections > max_failed:
        print("No internet after max attempts reached, reboot!")
        machine.reset()
    else:
        failed_connections = failed_connections + 1
    utime.sleep(10)


def start():
    try:
        print("Starting mq135")
        while True:
            data = mq135.modulMQ135()
            resp = esp_send_func.send_to_proxy(sensor_name="esp_mq135", value=data)
            utime.sleep(sleep_sec)
    except Exception as e:
        print("Start failed due to exception: {}".format(e))
        print("Reloading ESP!")
        machine.reset()
