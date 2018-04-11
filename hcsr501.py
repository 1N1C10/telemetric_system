from machine import Pin

def modulHCSR501():
    hc = Pin(2, Pin.IN)
    if hc.value() == 1:
        return hc.value()
    else:
        pass
