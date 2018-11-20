import machine
import dht
import time

d = dht.DHT22(machine.Pin(5))


def modulDHT22():
    time.sleep(2)
    d.measure()
    return d.humidity()
