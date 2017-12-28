import abc
from math import log

class TemperatureSensor(metaclass=abc.ABCMeta):
    """
    an abstract pressure sensor class
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

    def __init__(self, a, b, c, r2, vin, analog_input_interface):
        self.a = a
        self.b = b
        self.c = c
        self.r2 = r2
        self.vin = vin
        self.analog_input = analog_input_interface

    def _read_resistance(self, voltage_v):
        """
        returns the resistance of the thermistor.
        """
        return self.r2 * (self.vin/voltage_v - 1)

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

    def __init__(self, v1_v, t1_c, v2_v, t2_c, analog_input_interface):
        """
        temperature units are in Celsius since datasheets tend to prefer it over Kelvin.
        """
        # generate m and b for line formula based on two data points:
        # (t1, v1) and (t2, v2).
        self.gain = (t1_c - t2_c)/(v1_v - v2_v)
        self.offset = self.gain * (0 - v1_v) + t1_c
        self.analog_input = analog_input_interface

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

