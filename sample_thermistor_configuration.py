#!/usr/bin/env python3
"""
Sample configuration for reading a type K thermocouple over the following interface:
    AD8495TCAmplifier --> ADS1x15VoltageInputInterface --> ADS1015 --> BBI2CBus0
"""

import time
from object_oriented_hardware.ads1x15 import ADS1015
from object_oriented_hardware.ads1x15 import ADS1015VoltageInputInterface
from object_oriented_hardware.temperature_sensors import Thermistor
from object_oriented_hardware.beaglebone_i2c import BBI2CBus2

i2c_bus_2 = BBI2CBus2()

adc_bank = ADS1015(i2c_bus_2)
voltage_input = ADS1015VoltageInputInterface(adc_bank, channel_index=0)
thermistor = Thermistor(voltage_input)

while True:
    print(thermistor.read_temperature_c())
    time.sleep(0.5)

