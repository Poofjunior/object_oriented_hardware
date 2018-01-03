"""
smbus stub
"""

class SMBus(object):
    def __init__(self, bus):
        pass

    def write_byte_data(self, a, b, c):
        pass

    def write_i2c_block_data(self, a, b, c):
        pass

    def read_byte_data(self, a, b):
        return 0

    def read_i2c_block_data(self, a, b, c):
        return [0] * c

