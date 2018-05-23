
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
    print("Starting ds18b20")
    failed_attempts = 0
    while True:
        data = mp503.modulemp503()
        if data:
            resp = esp_send_func.send_to_ovh_metrics(sensor_name="esp_mp503",value=data)
            if not resp:
                if failed_attempts > max_failed:
                    machine.reset()
                else:
                    failed_attempts = failed_attempts + 1
        utime.sleep(sleep_sec)

