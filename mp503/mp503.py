from machine import ADC

adc = ADC(0)


def modulMP503():
    return adc.read()
