import machine
import dht
import time

d = dht.DHT22(machine.Pin(12))


def modulDHT22():
    time.sleep(2)
    return d.humidity()
