import esp_send_func
import mp503
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
        print("Starting mp503")
        while True:
            data = mp503.modulMP503()
            resp = esp_send_func.send_to_proxy(sensor_name="esp_mp503", value=data)
            utime.sleep(sleep_sec)
    except Exception as e:
        print("Start failed due to exception: {}".format(e))
        print("Reloading ESP!")
        machine.reset()
