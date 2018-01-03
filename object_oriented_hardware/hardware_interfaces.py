#!/usr/bin/env python3

import abc

class HardwareInterface(object):
    simulated = False

class DigitalInputInterface(HardwareInterface, metaclass=abc.ABCMeta):

    def __init__(self):
        self.simulated_input = False

    def read(self):
        """
        returns True or False
        """
        if self.simulated:
            return self.simulated_input
        else:
            return self._read()

    @abc.abstractmethod
    def _read(self):
        """
        Performs the actual read from the hardware. Implementation is hardware-specific.
        """
        pass

class AnalogInputInterface(HardwareInterface, metaclass=abc.ABCMeta):

    def __init__(self):
        self.simulated_input = 0.0

    def read(self):
        """
        returns the analog value. Units are implementation-specific.
        """
        if self.simulated:
            return self.simulated_input
        else:
            return self._read()

    @abc.abstractmethod
    def _read(self):
        """
        Performs the actual read from the hardware. Implementation is hardware-specific.
        """
        pass


class VoltageInputInterface(AnalogInputInterface):

    @abc.abstractmethod
    def _read(self):
        """
        returns an analog voltage in volts.
        """
        pass


class DigitalOutputInterface(HardwareInterface, metaclass=abc.ABCMeta):

    def __init__(self):
        self.simulated_output = False

    def write(self, value):
        """
        Writes value to the output.

        :param value: True or False
        """
        if self.simulated:
            self.simulated_output = value
        else:
            self._write(value)

    @abc.abstractmethod
    def _write(self, value):
        """
        Performs the actual write to hardware. Implementation is hardware-specific.
        """
        pass


class AnalogOutputInterface(HardwareInterface, metaclass=abc.ABCMeta):

    def __init__(self):
        self.simulated_output = 0.0

    def write(self, value):
        """
        Writes the analog value to the output. Units are implementation-specific.

        :param value: True or False
        """
        if self.simulated:
            self.simulated_output = value
        else:
            self._write(value)

    @abc.abstractmethod
    def _write(self, value):
        """
        Performs the actual write to hardware. Implementation is hardware-specific.
        """
        pass

