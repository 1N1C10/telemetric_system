import machine
adc = machine.ADC(0)


def modulLIGHT():
    raw = adc.read()
    return (((raw**2)*0.002268) - (0.3442*raw) + 27.853)
