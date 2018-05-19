import esp_send_func
import ds18b20
import machine
import utime


max_failed = 10
sleep_sec = 6

def start():
    failed_attempts = 0
    while True:
        data = ds18b20.modulDS18B20()
        if data:
            resp = esp_send_func.send_to_ovh_metrics(sensor_name="esp_ds18b20",value=data)
            if not resp:
                if failed_attempts > max_failed:
                    machine.reset()
                else:
                    failed_attempts = failed_attempts + 1
        utime.sleep(sleep_sec)

start()
