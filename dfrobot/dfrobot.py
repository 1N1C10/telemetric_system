from machine import Pin


def modulDFROBOT():
    df = Pin(2, Pin.IN)
    return df.value()