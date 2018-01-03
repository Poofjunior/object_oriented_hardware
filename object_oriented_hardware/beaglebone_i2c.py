#!/usr/bin/python
"""
Provides BBI2CBus0, BBI2CBus1, and BBI2CBus2 as singleton objects for reading a specific Beaglebone I2C bus.
"""

import abc
import logging
import threading
from .singleton import Singleton


def retry_on_fail(func):
    """
    a decorator that retries an exception-throwing BBI2C transaction up to 3 times before giving up.
    """
    def retry_on_fail_internal(self, *args, **kwargs):
        num_tries = 0
        while num_tries <= 3:
            try:
                with self._get_lock():
                    return func(self, *args, **kwargs)
                break
            except:
                num_tries += 1
                if num_tries < 3:
                    self.log.warning("Exception occurred performing an I2C {} on bus {}. Retrying."
                                     .format(func.__name__, self.bus_num))
                else:
                    self.log.warning("Giving up after {} attempts!".format(num_tries))
                    raise
    return retry_on_fail_internal


class BBI2CBus(metaclass=abc.ABCMeta):

    DEBUG = False # Set to True for more verbose i2c chatter.

    def __init__(self, bus_num):
        # smbus is not provided on all systems, so only import it if we try to instantiate an object.
        self.log = logging.getLogger(__name__)
        try:
            import smbus
        except ImportError:
            from object_oriented_hardware.stubs import smbus
            self.log.error("Cannot import smbus; Continuing with a stub.")
        assert 0 <= bus_num <= 2, "Error, valid i2c buses are only {}.".format([i for i in range(3)])
        self.bus = smbus.SMBus(bus_num)

    @abc.abstractmethod
    def _get_lock(self):
        """
        returns a lock for this i2c bus
        Abstract! To be implemented by the Singleton.
        """
        pass

    @retry_on_fail
    def write8(self, address, reg, value):
        "Writes an 8-bit value to the specified register/address. Retry on failures."
        if BBI2CBus.DEBUG:
            self.log.debug("I2C: Writing 0x{:02X} to register 0x{:02X} on device 0x{:02X}"
                            .format(value, reg, address))
        self.bus.write_byte_data(address, reg, value)

    @retry_on_fail
    def write16(self, address, reg, value):
        "Writes a 16-bit value to the specified register/address pair. Retry on failures."
        if BBI2CBus.DEBUG:
            self.log.debug("I2C: Writing 0x{:02X} to register 0x{:02X} on device 0x{:02X}"
                            .format(value, reg, address))
        self.bus.write_word_data(address, reg, value)

    @retry_on_fail
    def write_list(self, address, reg, values):
        "Writes an array of bytes using I2C format. Retry on failures."
        if BBI2CBus.DEBUG:
            self.log.debug("I2C: Writing {} to register 0x{:02X} on device 0x{:02X}"
                            .format(["0x{:02X}".format(i) for i in values], reg, address))
        self.bus.write_i2c_block_data(address, reg, values)

    @retry_on_fail
    def read8(self, address, reg):
        "Read an unsigned byte from the I2C device"
        value = self.bus.read_byte_data(address, reg)
        if BBI2CBus.DEBUG:
            self.log.debug("I2C: Read 0x{:02X} from register 0x{:02X} of device 0x{:02X}"
                            .format(value, reg, address))
        return value

    @retry_on_fail
    def read16(self, address, reg):
        "Reads an unsigned 16-bit value from the I2C device"
        value = self.bus.read_word_data(address, reg)
        if BBI2CBus.DEBUG:
            self.log.debug("I2C: Read 0x{:02X} from register 0x{:02X} of device 0x{:02X}"
                            .format(value, reg, address))
        return value

    @retry_on_fail
    def read_list(self, address, reg, length):
        "Read a list of bytes from the I2C device. Retry on failures."
        values = self.bus.read_i2c_block_data(address, reg, length)
        if BBI2CBus.DEBUG:
            self.log.debug("I2C: Read {} from register 0x{:02X} of device 0x{:02X}"
                            .format(["0x{:02X}".format(i) for i in values], reg, address))
        return values


class BBI2CBus0(Singleton, BBI2CBus):
    """
    A singleton class for the Beaglebone I2C Bus number 0
    """

    def init(self):
        """
        Singleton class requires us to write an init instead of an __init__
        """
        super().__init__(bus_num=0)
        self.bus_lock = threading.RLock()

    def __init__(self):
        pass

    def _get_lock(self):
        """
        returns a re-entrant thread lock for the bus number.
        """
        return self.bus_lock

class BBI2CBus1(Singleton, BBI2CBus):
    """
    A singleton class for the Beaglebone I2C Bus number 1
    """

    def init(self):
        """
        Singleton class requires us to write an init instead of an __init__
        """
        super().__init__(bus_num=1)
        self.bus_lock = threading.RLock()

    def _get_lock(self):
        """
        returns a re-entrant thread lock for the bus number.
        """
        return self.bus_lock


class BBI2CBus2(Singleton, BBI2CBus):
    """
    A singleton class for the Beaglebone I2C Bus number 2
    """

    def init(self):
        """
        Singleton class requires us to write an init instead of an __init__
        """
        super().__init__(bus_num=2)
        self.bus_lock = threading.RLock()

    def _get_lock(self):
        """
        returns a re-entrant thread lock for the bus number.
        """
        return self.bus_lock

