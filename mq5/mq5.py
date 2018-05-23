from machine import ADC
import utime


def modulmq5():

    adc = ADC(0)
    r0 = 1.5
   
    sensor_val = adc.read()
    sensor_volt = (sensor_val/1024) * 3.3
    rs_gas = (3.3 - sensor_volt)/sensor_volt
    ratio = rs_gas/r0
    ppm = ((10.934*ratio)** (-0.211))
    return ppm


