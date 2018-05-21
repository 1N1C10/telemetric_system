from machine import ADC
import utime

def modulemp503():

    adc = ADC(0)
    r0 = 250
    val = adc.read()
    ratio = r0/(1024 - r0) * (1024 - val)/val
    ppm = (1.0413 * (ratio))**(-0.711)
    return ppm