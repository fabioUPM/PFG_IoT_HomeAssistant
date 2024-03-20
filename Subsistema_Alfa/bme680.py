# The MIT License (MIT)
#
# Copyright (c) 2017 ladyada for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# We have a lot of attributes for this complex sensor.
# pylint: disable=too-many-instance-attributes

"""
`bme680` - BME680 - Temperature, Humidity, Pressure & Gas Sensor
================================================================
MicroPython driver from BME680 air quality sensor, based on Adafruit_bme680
* Author(s): Limor 'Ladyada' Fried of Adafruit
             Jeff Raber (SPI support)
             and many more contributors
"""

import time
import math
from micropython import const
from ubinascii import hexlify as hex
try:
    import struct
except ImportError:
    import ustruct as struct
    
#    I2C ADDRESS/BITS/SETTINGS NEW
#    -----------------------------------------------------------------------
_BME68X_ENABLE_HEATER = const(0x00)
_BME68X_DISABLE_HEATER = const(0x01)
_BME68X_DISABLE_GAS_MEAS = const(0x00)
_BME68X_ENABLE_GAS_MEAS_L = const(0x01)
_BME68X_ENABLE_GAS_MEAS_H = const(0x02)
_BME68X_SLEEP_MODE = const(0)
_BME68X_FORCED_MODE = const(1)
_BME68X_VARIANT_GAS_LOW = const(0x00)
_BME68X_VARIANT_GAS_HIGH = const(0x01)
_BME68X_HCTRL_MSK = const(0x08)
_BME68X_HCTRL_POS = const(3)
_BME68X_NBCONV_MSK = const(0x0F)
_BME68X_RUN_GAS_MSK = const(0x30)
_BME68X_RUN_GAS_POS = const(4)
_BME68X_MODE_MSK = const(0x03)
_BME68X_PERIOD_POLL = const(10000)
_BME68X_REG_CTRL_GAS_0 = const(0x70)
_BME68X_REG_CTRL_GAS_1 = const(0x71)

#    I2C ADDRESS/BITS/SETTINGS
#    -----------------------------------------------------------------------
_BME680_CHIPID = const(0x61)

_BME680_REG_CHIPID = const(0xD0)
_BME68X_REG_VARIANT = const(0xF0)
_BME680_BME680_COEFF_ADDR1 = const(0x89)
_BME680_BME680_COEFF_ADDR2 = const(0xE1)
_BME680_BME680_RES_HEAT_0 = const(0x5A)
_BME680_BME680_GAS_WAIT_0 = const(0x64)

_BME680_REG_SOFTRESET = const(0xE0)
_BME680_REG_CTRL_GAS = const(0x71)
_BME680_REG_CTRL_HUM = const(0x72)
_BME280_REG_STATUS = const(0xF3)
_BME680_REG_CTRL_MEAS = const(0x74)
_BME680_REG_CONFIG = const(0x75)

_BME680_REG_PAGE_SELECT = const(0x73)
_BME680_REG_MEAS_STATUS = const(0x1D)
_BME680_REG_PDATA = const(0x1F)
_BME680_REG_TDATA = const(0x22)
_BME680_REG_HDATA = const(0x25)

_BME680_SAMPLERATES = (0, 1, 2, 4, 8, 16)
_BME680_FILTERSIZES = (0, 1, 3, 7, 15, 31, 63, 127)

_BME680_RUNGAS = const(0x10)

_LOOKUP_TABLE_1 = (2147483647.0, 2147483647.0, 2147483647.0, 2147483647.0, 2147483647.0,
                   2126008810.0, 2147483647.0, 2130303777.0, 2147483647.0, 2147483647.0,
                   2143188679.0, 2136746228.0, 2147483647.0, 2126008810.0, 2147483647.0,
                   2147483647.0)

_LOOKUP_TABLE_2 = (4096000000.0, 2048000000.0, 1024000000.0, 512000000.0, 255744255.0, 127110228.0,
                   64000000.0, 32258064.0, 16016016.0, 8000000.0, 4000000.0, 2000000.0, 1000000.0,
                   500000.0, 250000.0, 125000.0)

def bme_set_bits(reg_data, bitname_msk, bitname_pos, data):
    """
    Macro to set bits
    data2 = data << bitname_pos
    set masked bits from data2 in reg_data
    """
    return (reg_data & ~bitname_msk) | ((data << bitname_pos) & bitname_msk)

def bme_set_bits_pos_0(reg_data, bitname_msk, data):
    """
    Macro to set bits starting from position 0
    set masked bits from data in reg_data
    """
    return (reg_data & ~bitname_msk) | (data & bitname_msk)



def _read24(arr):
    """Parse an unsigned 24-bit value as a floating point and return it."""
    ret = 0.0
    #print([hex(i) for i in arr])
    for b in arr:
        ret *= 256.0
        ret += float(b & 0xFF)
    return ret


class Adafruit_BME680:
    """Driver from BME680 air quality sensor
       :param int refresh_rate: Maximum number of readings per second. Faster property reads
         will be from the previous reading."""
    def __init__(self, *, refresh_rate=10):
        """Check the BME680 was found, read the coefficients and enable the sensor for continuous
           reads."""
        self._write(_BME680_REG_SOFTRESET, [0xB6])
        time.sleep(0.005)

        # Check device ID.
        chip_id = self._read_byte(_BME680_REG_CHIPID)
        if chip_id != _BME680_CHIPID:
            raise RuntimeError('Failed to find BME680! Chip ID 0x%x' % chip_id)
        
        # Get variant
        self._chip_variant = self._read_byte(_BME68X_REG_VARIANT)

        self._read_calibration()

        # set up heater
        self._write(_BME680_BME680_RES_HEAT_0, [0x73])
        self._write(_BME680_BME680_GAS_WAIT_0, [0x65])

        self.sea_level_pressure = 1013.25
        """Pressure in hectoPascals at sea level. Used to calibrate ``altitude``."""

        # Default oversampling and filter register values.
        self._pressure_oversample = 0b011
        self._temp_oversample = 0b100
        self._humidity_oversample = 0b010
        self._filter = 0b010
        
        # Gas measurements, as a mask applied to _BME680_RUNGAS
        self._run_gas = 0xFF

        self._adc_pres = None
        self._adc_temp = None
        self._adc_hum = None
        self._adc_gas = None
        self._gas_range = None
        self._t_fine = None

        self._last_reading = time.ticks_ms()
        self._min_refresh_time = 1000 // refresh_rate
        
        self._amb_temp = 25  # Copy required parameters from reference bme68x_dev struct
        self.set_gas_heater(320, 150)  # heater 320 deg C for 150 msec

    @property
    def pressure_oversample(self):
        """The oversampling for pressure sensor"""
        return _BME680_SAMPLERATES[self._pressure_oversample]

    @pressure_oversample.setter
    def pressure_oversample(self, sample_rate):
        if sample_rate in _BME680_SAMPLERATES:
            self._pressure_oversample = _BME680_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")

    @property
    def humidity_oversample(self):
        """The oversampling for humidity sensor"""
        return _BME680_SAMPLERATES[self._humidity_oversample]

    @humidity_oversample.setter
    def humidity_oversample(self, sample_rate):
        if sample_rate in _BME680_SAMPLERATES:
            self._humidity_oversample = _BME680_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")

    @property
    def temperature_oversample(self):
        """The oversampling for temperature sensor"""
        return _BME680_SAMPLERATES[self._temp_oversample]

    @temperature_oversample.setter
    def temperature_oversample(self, sample_rate):
        if sample_rate in _BME680_SAMPLERATES:
            self._temp_oversample = _BME680_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")

    @property
    def filter_size(self):
        """The filter size for the built in IIR filter"""
        return _BME680_FILTERSIZES[self._filter]

    @filter_size.setter
    def filter_size(self, size):
        if size in _BME680_FILTERSIZES:
            self._filter = _BME680_FILTERSIZES[size]
        else:
            raise RuntimeError("Invalid size")

    @property
    def temperature(self):
        """The compensated temperature in degrees celsius."""
        self._perform_reading()
        calc_temp = (((self._t_fine * 5) + 128) / 256)
        return calc_temp / 100

    @property
    def pressure(self):
        """The barometric pressure in hectoPascals"""
        self._perform_reading()
        var1 = (self._t_fine / 2) - 64000
        var2 = ((var1 / 4) * (var1 / 4)) / 2048
        var2 = (var2 * self._pressure_calibration[5]) / 4
        var2 = var2 + (var1 * self._pressure_calibration[4] * 2)
        var2 = (var2 / 4) + (self._pressure_calibration[3] * 65536)
        var1 = (((((var1 / 4) * (var1 / 4)) / 8192) *
                (self._pressure_calibration[2] * 32) / 8) +
                ((self._pressure_calibration[1] * var1) / 2))
        var1 = var1 / 262144
        var1 = ((32768 + var1) * self._pressure_calibration[0]) / 32768
        calc_pres = 1048576 - self._adc_pres
        calc_pres = (calc_pres - (var2 / 4096)) * 3125
        calc_pres = (calc_pres / var1) * 2
        var1 = (self._pressure_calibration[8] * (((calc_pres / 8) * (calc_pres / 8)) / 8192)) / 4096
        var2 = ((calc_pres / 4) * self._pressure_calibration[7]) / 8192
        var3 = (((calc_pres / 256) ** 3) * self._pressure_calibration[9]) / 131072
        calc_pres += ((var1 + var2 + var3 + (self._pressure_calibration[6] * 128)) / 16)
        return calc_pres/100

    @property
    def humidity(self):
        """The relative humidity in RH %"""
        self._perform_reading()
        temp_scaled = ((self._t_fine * 5) + 128) / 256
        var1 = ((self._adc_hum - (self._humidity_calibration[0] * 16)) -
                ((temp_scaled * self._humidity_calibration[2]) / 200))
        var2 = (self._humidity_calibration[1] *
                (((temp_scaled * self._humidity_calibration[3]) / 100) +
                 (((temp_scaled * ((temp_scaled * self._humidity_calibration[4]) / 100)) /
                   64) / 100) + 16384)) / 1024
        var3 = var1 * var2
        var4 = self._humidity_calibration[5] * 128
        var4 = (var4 + ((temp_scaled * self._humidity_calibration[6]) / 100)) / 16
        var5 = ((var3 / 16384) * (var3 / 16384)) / 1024
        var6 = (var4 * var5) / 2
        calc_hum = (((var3 + var6) / 1024) * 1000) / 4096
        calc_hum /= 1000  # get back to RH

        if calc_hum > 100:
            calc_hum = 100
        if calc_hum < 0:
            calc_hum = 0
        return calc_hum

    @property
    def altitude(self):
        """The altitude based on current ``pressure`` vs the sea level pressure
           (``sea_level_pressure``) - which you must enter ahead of time)"""
        pressure = self.pressure # in Si units for hPascal
        return 44330 * (1.0 - math.pow(pressure / self.sea_level_pressure, 0.1903))

    @property
    def gas(self):
        """The gas resistance in ohms"""
        self._perform_reading()
        if self._chip_variant == 0x01:
            # taken from https://github.com/BoschSensortec/BME68x-Sensor-API
            var1 = 262144 >> self._gas_range
            var2 = self._adc_gas - 512
            var2 *= 3
            var2 = 4096 + var2
            calc_gas_res = (10000 * var1) / var2
            calc_gas_res = calc_gas_res * 100
        else:
            var1 = ((1340 + (5 * self._sw_err)) * (_LOOKUP_TABLE_1[self._gas_range])) / 65536
            var2 = ((self._adc_gas * 32768) - 16777216) + var1
            var3 = (_LOOKUP_TABLE_2[self._gas_range] * var1) / 512
            calc_gas_res = (var3 + (var2 / 2)) / var2
        return int(calc_gas_res)
    

    def _perform_reading(self):
        """Perform a single-shot reading from the sensor and fill internal data structure for
           calculations"""
        expired = time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1)
        if 0 <= expired < self._min_refresh_time:
            time.sleep_ms(self._min_refresh_time - expired)

        # set filter
        self._write(_BME680_REG_CONFIG, [self._filter << 2])
        # turn on temp oversample & pressure oversample
        self._write(_BME680_REG_CTRL_MEAS,
                    [(self._temp_oversample << 5)|(self._pressure_oversample << 2)])
        # turn on humidity oversample
        self._write(_BME680_REG_CTRL_HUM, [self._humidity_oversample])
        # gas measurements enabled
        if self._chip_variant == 0x01:
            self._write(_BME680_REG_CTRL_GAS, [(self._run_gas & _BME680_RUNGAS) << 1])
        else:
            self._write(_BME680_REG_CTRL_GAS, [(self._run_gas & _BME680_RUNGAS)])

        ctrl = self._read_byte(_BME680_REG_CTRL_MEAS)
        ctrl = (ctrl & 0xFC) | 0x01  # enable single shot!
        self._write(_BME680_REG_CTRL_MEAS, [ctrl])
        new_data = False
        while not new_data:
            #data = self._read(_BME680_REG_MEAS_STATUS, 15)
            data = self._read(_BME680_REG_MEAS_STATUS, 17)
            new_data = data[0] & 0x80 != 0
            time.sleep(0.005)
        self._last_reading = time.ticks_ms()

        self._adc_pres = _read24(data[2:5]) / 16
        self._adc_temp = _read24(data[5:8]) / 16
        self._adc_hum = struct.unpack('>H', bytes(data[8:10]))[0]
        #self._adc_gas = int(struct.unpack('>H', bytes(data[13:15]))[0] / 64)
        #self._gas_range = data[14] & 0x0F
        if self._chip_variant == 0x01:
            self._adc_gas = int(struct.unpack(">H", bytes(data[15:17]))[0] / 64)
            self._gas_range = data[16] & 0x0F
        else:
            self._adc_gas = int(struct.unpack(">H", bytes(data[13:15]))[0] / 64)
            self._gas_range = data[14] & 0x0F

        var1 = (self._adc_temp / 8) - (self._temp_calibration[0] * 2)
        var2 = (var1 * self._temp_calibration[1]) / 2048
        var3 = ((var1 / 2) * (var1 / 2)) / 4096
        var3 = (var3 * self._temp_calibration[2] * 16) / 16384

        self._t_fine = int(var2 + var3)

    def _read_calibration(self):
        """Read & save the calibration coefficients"""
        coeff = self._read(_BME680_BME680_COEFF_ADDR1, 25)
        coeff += self._read(_BME680_BME680_COEFF_ADDR2, 16)

        coeff = list(struct.unpack('<hbBHhbBhhbbHhhBBBHbbbBbHhbb', bytes(coeff[1:39])))
        # print("\n\n",coeff)
        coeff = [float(i) for i in coeff]
        self._temp_calibration = [coeff[x] for x in [23, 0, 1]]
        self._pressure_calibration = [coeff[x] for x in [3, 4, 5, 7, 8, 10, 9, 12, 13, 14]]
        self._humidity_calibration = [coeff[x] for x in [17, 16, 18, 19, 20, 21, 22]]
        self._gas_calibration = [coeff[x] for x in [25, 24, 26]]

        # flip around H1 & H2
        self._humidity_calibration[1] *= 16
        self._humidity_calibration[1] += self._humidity_calibration[0] % 16
        self._humidity_calibration[0] /= 16

        self._heat_range = (self._read_byte(0x02) & 0x30) / 16
        self._heat_val = self._read_byte(0x00)
        self._sw_err = (self._read_byte(0x04) & 0xF0) / 16

    def _read_byte(self, register):
        """Read a byte register value and return it"""
        return self._read(register, 1)[0]

    def _read(self, register, length):
        raise NotImplementedError()

    def _write(self, register, values):
        raise NotImplementedError()

    def set_gas_heater(self, heater_temp: int, heater_time: int) -> bool:
        """
        Enable and configure gas reading + heater (None disables)
        :param  heater_temp: Desired temperature in degrees Centigrade
        :param  heater_time: Time to keep heater on in milliseconds
        :return: True on success, False on failure
        """
        try:
            if (heater_temp is None) or (heater_time is None):
                self._set_heatr_conf(heater_temp or 0, heater_time or 0, enable=False)
            else:
                self._set_heatr_conf(heater_temp, heater_time)
        except OSError:
            return False
        return True
    
    
    def _set_heatr_conf(
        self, heater_temp: int, heater_time: int, enable: bool = True
    ) -> None:
        # restrict to BME68X_FORCED_MODE
        op_mode: int = _BME68X_FORCED_MODE
        nb_conv: int = 0
        hctrl: int = _BME68X_ENABLE_HEATER
        run_gas: int = 0
        ctrl_gas_data_0: int = 0
        ctrl_gas_data_1: int = 0
        try:
            self._set_op_mode(_BME68X_SLEEP_MODE)
            self._set_conf(heater_temp, heater_time, op_mode)
            ctrl_gas_data_0 = self._read_byte(_BME68X_REG_CTRL_GAS_0)
            ctrl_gas_data_1 = self._read_byte(_BME68X_REG_CTRL_GAS_1)
            if enable:
                hctrl = _BME68X_ENABLE_HEATER
                if self._chip_variant == _BME68X_VARIANT_GAS_HIGH:
                    run_gas = _BME68X_ENABLE_GAS_MEAS_H
                else:
                    run_gas = _BME68X_ENABLE_GAS_MEAS_L
            else:
                hctrl = _BME68X_DISABLE_HEATER
                run_gas = _BME68X_DISABLE_GAS_MEAS
            self._run_gas = ~(run_gas - 1)

            ctrl_gas_data_0 = bme_set_bits(
                ctrl_gas_data_0, _BME68X_HCTRL_MSK, _BME68X_HCTRL_POS, hctrl
            )
            ctrl_gas_data_1 = bme_set_bits_pos_0(
                ctrl_gas_data_1, _BME68X_NBCONV_MSK, nb_conv
            )
            ctrl_gas_data_1 = bme_set_bits(
                ctrl_gas_data_1, _BME68X_RUN_GAS_MSK, _BME68X_RUN_GAS_POS, run_gas
            )
            self._write(_BME68X_REG_CTRL_GAS_0, [ctrl_gas_data_0])
            self._write(_BME68X_REG_CTRL_GAS_1, [ctrl_gas_data_1])
            # HELP check this
        finally:
            self._set_op_mode(_BME68X_FORCED_MODE)
    
    
    def _set_op_mode(self, op_mode: int) -> None:
        """
        * @brief This API is used to set the operation mode of the sensor
        """
        tmp_pow_mode: int = 0
        pow_mode: int = _BME68X_FORCED_MODE
        # Call until in sleep

        # was a do {} while() loop
        while pow_mode != _BME68X_SLEEP_MODE:
            tmp_pow_mode = self._read_byte(_BME680_REG_CTRL_MEAS)
            # Put to sleep before changing mode
            pow_mode = tmp_pow_mode & _BME68X_MODE_MSK
            if pow_mode != _BME68X_SLEEP_MODE:
                tmp_pow_mode &= ~_BME68X_MODE_MSK  # Set to sleep
                self._write(_BME680_REG_CTRL_MEAS, [tmp_pow_mode])
                # dev->delay_us(_BME68X_PERIOD_POLL, dev->intf_ptr)  # HELP
                delay_microseconds(_BME68X_PERIOD_POLL)
        # Already in sleep
        if op_mode != _BME68X_SLEEP_MODE:
            tmp_pow_mode = (tmp_pow_mode & ~_BME68X_MODE_MSK) | (
                op_mode & _BME68X_MODE_MSK
            )
            self._write(_BME680_REG_CTRL_MEAS, [tmp_pow_mode])
            
            
    def _set_conf(self, heater_temp: int, heater_time: int, op_mode: int) -> None:
        """
        This internal API is used to set heater configurations
        """

        if op_mode != _BME68X_FORCED_MODE:
            raise OSError("GasHeaterException: _set_conf not forced mode")
        rh_reg_data: int = self._calc_res_heat(heater_temp)
        gw_reg_data: int = self._calc_gas_wait(heater_time)
        self._write(_BME680_BME680_RES_HEAT_0, [rh_reg_data])
        self._write(_BME680_BME680_GAS_WAIT_0, [gw_reg_data])
        
    def _calc_res_heat(self, temp: int) -> int:
        """
        This internal API is used to calculate the heater resistance value using float
        """
        gh1: int = self._gas_calibration[0]
        gh2: int = self._gas_calibration[1]
        gh3: int = self._gas_calibration[2]
        htr: int = self._heat_range
        htv: int = self._heat_val
        amb: int = self._amb_temp

        temp = min(temp, 400)  # Cap temperature

        var1: int = ((int(amb) * gh3) / 1000) * 256
        var2: int = (gh1 + 784) * (((((gh2 + 154009) * temp * 5) / 100) + 3276800) / 10)
        var3: int = var1 + (var2 / 2)
        var4: int = var3 / (htr + 4)
        var5: int = (131 * htv) + 65536
        heatr_res_x100: int = int(((var4 / var5) - 250) * 34)
        heatr_res: int = int((heatr_res_x100 + 50) / 100)

        return heatr_res

    def _calc_res_heat(self, temp: int) -> int:
        """
        This internal API is used to calculate the heater resistance value
        """
        gh1: float = float(self._gas_calibration[0])
        gh2: float = float(self._gas_calibration[1])
        gh3: float = float(self._gas_calibration[2])
        htr: float = float(self._heat_range)
        htv: float = float(self._heat_val)
        amb: float = float(self._amb_temp)

        temp = min(temp, 400)  # Cap temperature

        var1: float = (gh1 / (16.0)) + 49.0
        var2: float = ((gh2 / (32768.0)) * (0.0005)) + 0.00235
        var3: float = gh3 / (1024.0)
        var4: float = var1 * (1.0 + (var2 * float(temp)))
        var5: float = var4 + (var3 * amb)
        res_heat: int = int(
            3.4 * ((var5 * (4 / (4 + htr)) * (1 / (1 + (htv * 0.002)))) - 25)
        )
        return res_heat

    def _calc_gas_wait(self, dur: int) -> int:
        """
        This internal API is used to calculate the gas wait
        """
        factor: int = 0
        durval: int = 0xFF  # Max duration

        if dur >= 0xFC0:
            return durval
        while dur > 0x3F:
            dur = dur / 4
            factor += 1
        durval = int(dur + (factor * 64))
        return durval
    
    

    
class BME680_I2C(Adafruit_BME680):
    """Driver for I2C connected BME680.
        :param i2c: I2C device object
        :param int address: I2C device address
        :param bool debug: Print debug statements when True.
        :param int refresh_rate: Maximum number of readings per second. Faster property reads
          will be from the previous reading."""
    def __init__(self, i2c, address=0x76, debug=False, *, refresh_rate=10):
        """Initialize the I2C device at the 'address' given"""
        self._i2c = i2c
        self._address = address
        self._debug = debug
        super().__init__(refresh_rate=refresh_rate)

    def _read(self, register, length):
        """Returns an array of 'length' bytes from the 'register'"""
        result = bytearray(length)
        self._i2c.readfrom_mem_into(self._address, register & 0xff, result)
        if self._debug:
            print("\t${:x} read ".format(register), " ".join(["{:02x}".format(i) for i in result]))
        return result

    def _write(self, register, values):
        """Writes an array of 'length' bytes to the 'register'"""
        if self._debug:
            print("\t${:x} write".format(register), " ".join(["{:02x}".format(i) for i in values]))
        for value in values:
            self._i2c.writeto_mem(self._address, register, bytearray([value & 0xFF]))
            register += 1


class BME680_SPI(Adafruit_BME680):
    """Driver for SPI connected BME680.
        :param spi: SPI device object, configured
        :param cs: Chip Select Pin object, configured to OUT mode
        :param bool debug: Print debug statements when True.
        :param int refresh_rate: Maximum number of readings per second. Faster property reads
          will be from the previous reading.
      """

    def __init__(self, spi, cs, debug=False, *, refresh_rate=10):
        self._spi = spi
        self._cs = cs
        self._debug = debug
        self._cs(1)
        super().__init__(refresh_rate=refresh_rate)

    def _read(self, register, length):
        if register != _BME680_REG_PAGE_SELECT:
            # _BME680_REG_PAGE_SELECT exists in both SPI memory pages
            # For all other registers, we must set the correct memory page
            self._set_spi_mem_page(register)
        register = (register | 0x80) & 0xFF  # Read single, bit 7 high.

        try:
            self._cs(0)
            self._spi.write(bytearray([register]))  # pylint: disable=no-member
            result = bytearray(length)
            self._spi.readinto(result)  # pylint: disable=no-member
            if self._debug:
                print("\t${:x} read ".format(register), " ".join(["{:02x}".format(i) for i in result]))
        except Exception as e:
            print (e)
            result = None
        finally:
            self._cs(1)
        return result

    def _write(self, register, values):
        if register != _BME680_REG_PAGE_SELECT:
            # _BME680_REG_PAGE_SELECT exists in both SPI memory pages
            # For all other registers, we must set the correct memory page
            self._set_spi_mem_page(register)
        register &= 0x7F  # Write, bit 7 low.
        try:
            self._cs(0)
            buffer = bytearray(2 * len(values))
            for i, value in enumerate(values):
                buffer[2 * i] = register + i
                buffer[2 * i + 1] = value & 0xFF
            self._spi.write(buffer)  # pylint: disable=no-member
            if self._debug:
                print("\t${:x} write".format(register), " ".join(["{:02x}".format(i) for i in values]))
        except Exception as e:
            print (e)
        finally:
            self._cs(1)

    def _set_spi_mem_page(self, register):
        spi_mem_page = 0x00
        if register < 0x80:
            spi_mem_page = 0x10
        self._write(_BME680_REG_PAGE_SELECT, [spi_mem_page])