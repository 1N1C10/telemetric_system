import esp_send_func
import mq135
import machine
import utime


max_failed = 10
sleep_sec = 6

def start():
    failed_attempts = 0
    while True:
        data = mq135.modulmq135()
        if data:
            resp = esp_send_func.send_to_ovh_metrics(sensor_name="esp_mq135",value=mq135.modulmq135())
            if not resp:
                if failed_attempts > max_failed:
                    machine.reset()
                else:
                    failed_attempts = failed_attempts + 1
        utime.sleep(sleep_sec)

start()
