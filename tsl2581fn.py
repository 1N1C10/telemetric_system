from machine import I2C, Pin
import utime

command_cmd = 0x80
control = 0x00
control_poweron = 0x01
timing = 0x01
integrationtime_400ms = 0x6C
adc_en = 0X02
interrupt = 0X02
intr_inter_mode = 0X1F
analog = 0X07
gain_16x = 0x02
data0low = 0X14
data0high = 0X15
data1low = 0X16
data1high = 0X17
transaction = 0x40
nom_integ_cycle = 148
ch_scale = 16
ch0gain128x = 107
ch1gain128x = 115
ratio_scale = 9
lux_scale = 16

K1C = 0x009A
B1C = 0x2148
M1C = 0x3d71
K2C = 0x00c3
B2C = 0x2a37
M2C = 0x5b30
K3C = 0x00e6
B3C = 0x18ef
M3C = 0x2db9
K4C = 0x0114
B4C = 0x0fdf
M4C = 0x199a
K5C = 0x0114
B5C = 0x0000
M5C = 0x0000


def read_channel():
    utime.sleep_ms(450)
    low = i2c.readfrom_mem(address, command_cmd | transaction | data0low, 8)
    high = i2c.readfrom_mem(address, command_cmd | transaction | data0high, 8)
    ch0 = high * 256 + low

    low = i2c.readfrom_mem(address, command_cmd | transaction | data1low, 8)
    high = i2c.readfrom_mem(address, command_cmd | transaction | data1high, 8)
    ch1 = high * 256 + low

    return ch0, ch1


def calculate_lux(igain, tintcycles, ch0, ch1):
    chscale1 = 0
    ratio1 = 0
    b = 0
    m = 0
    if tintcycles == nom_integ_cycle:
        chscale0 = 65536
    else:
        chscale0 = (nom_integ_cycle << ch_scale) / tintcycles

    if igain == 0:
        chscale1 = chscale0
    elif igain == 1:
        chscale0 = chscale0 >> 3
        chscale1 = chscale0
    elif igain == 2:
        chscale0 = chscale0 >> 4
        chscale1 = chscale0
    elif igain == 3:
        chscale1 = chscale0 / ch0gain128x
        chscale0 = chscale0 / ch1gain128x

    channel0 = (ch0 * chscale0) >> ch_scale
    channel1 = (ch1 * chscale1) >> ch_scale

    if channel0 != 0:
        ratio1 = (channel1 << (ratio_scale + 1)) / channel0

    ratio = (ratio1 + 1) >> 1

    if (ratio >= 0) and (ratio <= K1C):
        b = B1C
        m = M1C
    elif ratio <= K2C:
        b = B2C
        m = M2C
    elif ratio <= K3C:
        b = B3C
        m = M3C
    elif ratio <= K4C:
        b = B4C
        m = M4C
    elif ratio > K5C:
        b = B5C
        m = M5C
    temp = ((channel0 * b) - (channel1 * m))
    temp = temp + 32768
    lux_temp = temp >> lux_scale
    return lux_temp


# Init
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
addresses = i2c.scan()
address = addresses[0]

# Power on
i2c.writeto_mem(address, command_cmd | control, bytearray([control_poweron]))
utime.sleep_ms(2000)

# CONFIG
# 400 ms
i2c.writeto_mem(address, command_cmd | timing, bytearray([integrationtime_400ms]))

# Part of config
i2c.writeto_mem(address, command_cmd | control, bytearray([adc_en | control_poweron]))

# Every ADC cycle generates interrupt
i2c.writeto_mem(address, command_cmd | interrupt, bytearray([intr_inter_mode]))

# Gain = 16
i2c.writeto_mem(address, command_cmd | analog, bytearray([gain_16x]))


def modultsl2581fn():
    # Reading data
    ch0, ch1 = read_channel()

    # Calculating lux
    lux_final = calculate_lux(2, nom_integ_cycle, ch0, ch1)

    return lux_final