from machine import ADC


def modulMP503():
    adc = ADC(0)
    value = adc.read()
    return value
