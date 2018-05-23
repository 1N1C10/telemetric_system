from machine import Pin


def modulDFROBOT():
    df = Pin(2, Pin.IN)
    if df.value() == 1:
        return df.value()
    else:
        pass