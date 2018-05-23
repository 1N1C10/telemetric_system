import utime
import machine
import onewire, ds18x20

dat = machine.Pin(12)
ds = ds18x20.DS18X20(onewire.OneWire(dat))
roms = ds.scan()
rom = roms[0]


def modulDS18B20():
    ds.convert_temp()
    utime.sleep_ms(750)
    return ds.read_temp(rom)
