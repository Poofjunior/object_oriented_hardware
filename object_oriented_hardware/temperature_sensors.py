#!/usr/bin/env python3

import abc
from math import log

class TemperatureSensor(metaclass=abc.ABCMeta):
    """
    an abstract temperature sensor class
    """

    ABSOLUTE_ZERO_OFFSET_C = 273.15

    def __init__(self):
        pass

    @abc.abstractmethod
    def read_temperature_k(self):
        """
        returns the temperature in Kelvin
        """
        pass

    def read_temperature_c(self):
        """
        returns the temperature in degrees Celsius
        """
        return self.read_temperature_k() - TemperatureSensor.ABSOLUTE_ZERO_OFFSET_C

    def read_temperature_f(self):
        """
        returns the temperature in degrees Fahrenheit
        """
        return self.read_temperature_c() * (9.0/5.0) + 32.0


class Thermistor(TemperatureSensor):
    """
    a thermistor class

    Note: thermistor is assumed to be read from a resistor divider configuration with
          a supplementary pulldown resistor added. Pullup value must be provided on init.
    """

    def __init__(self, a, b, c, r2_ohms, vin_v, voltage_input_interface):
        """
        Initialize a Thermistor in voltage divider configuration.
        Note: thermistor is set as the pullup resistor in the voltage divider.

        :param a: Steinhart–Hart equation constant A
        :param b: Steinhart–Hart equation constant B
        :param c: Steinhart–Hart equation constant C
        :param r2_ohms: pulldown resistor resistance in ohms
        :param vin_v: resistor divider input voltage in volts
        :param voltage_input_interface: analog input where the voltage-divider input will be measured
        """
        self.a = a
        self.b = b
        self.c = c
        self.r2_ohms = r2_ohms
        self.vin_v = vin_v
        self.analog_input = voltage_input_interface

    def _read_resistance(self, voltage_v):
        """
        returns the resistance of the thermistor in ohms.
        """
        return self.r2_ohms * (self.vin_v/voltage_v - 1)

    def read_temperature_k(self):
        """
        returns the temperature in Kelvin
        Note: implements abstract base class read_temperature_k
        """
        voltage_v = self.analog_input.read()
        r1_ohms = self._read_resistance(voltage_v)
        return 1.0/(self.a + self.b * log(r1_ohms) + self.c * log(r1_ohms)**3)


class AnalogTemperatureSensor(TemperatureSensor):
    """
    a linear analog-output-based temperature sensor.
    """

    def __init__(self, voltage_input_interface, v1_v, t1_c, v2_v, t2_c):
        """
        Establishing the voltage-to-pressure measurement requires two datapoints:
        (v1_v, t1_c) and (v2_v, t2_c), which can be derived from the sensor specs.
        Temperature units are in Celsius since datasheets tend to prefer it over Kelvin.

        :param v1_v: voltage measurement (in volts) corresponding to t1_c
        :param t1_c: temperature measurement (in Celsius) corresponding to v1_v
        :param v2_v: voltage measurement (in volts) corresponding to t2_c
        :param t2_c: temperature measurement (in Celsius) corresponding to v2_v
        :param voltage_input_interface: the analog input from which the voltage will be measured
        """
        # generate slop and y-intercept for line formula based on two data points:
        self.gain = (t1_c - t2_c)/(v1_v - v2_v)
        self.offset = self.gain * (0 - v1_v) + t1_c
        self.analog_input = voltage_input_interface

    def read_temperature_c(self):
        """
        returns the temperature in Celsius.
        Note: overrides base class read_temperature_c
        """
        voltage_v = self.analog_input.read()
        return self.gain * voltage_v + self.offset

    def read_temperature_k(self):
        """
        returns the temperature in Kelvin
        Note: implements abstract base class read_temperature_k
        """
        return self.read_temperature_c() + TemperatureSensor.ABSOLUTE_ZERO_OFFSET_C


class AD8495TCAmplifier(AnalogTemperatureSensor):

    def __init__(self, voltage_input_interface, v1_v=1.25, t1_c=0.0, v2_v=1.5, t2_c=50):
        super().__init__(voltage_input_interface, v1_v, t1_c, v2_v, t2_c)

