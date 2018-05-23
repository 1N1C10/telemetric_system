from machine import ADC

RLOAD = 4700
RZERO = 7300
PARA = 116.6020682
PARB = 2.769034857


def modulmq135():
    mq = ADC(0)
    value = mq.read()
    resistance = (1023 / (value - 1)) * RLOAD
    ppm = PARA * ((resistance / RZERO) ** -PARB)
    return ppm
