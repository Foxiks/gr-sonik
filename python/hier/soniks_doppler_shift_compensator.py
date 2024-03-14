# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks Doppler shift compensator
# GNU Radio version: 3.10.7.0

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import gr
import soniks.doppler







class soniks_doppler_shift_compensator(gr.hier_block2):
    def __init__(self, c_rf=435870000, inv=False, s_alt='0', s_lat='0', s_lon='0', samp_rate=48000, sat_name='GEOSCAN', tle_p='/path/to/tle.txt', up=1000):
        gr.hier_block2.__init__(
            self, "Soniks Doppler shift compensator",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.c_rf = c_rf
        self.inv = inv
        self.s_alt = s_alt
        self.s_lat = s_lat
        self.s_lon = s_lon
        self.samp_rate = samp_rate
        self.sat_name = sat_name
        self.tle_p = tle_p
        self.up = up

        ##################################################
        # Blocks
        ##################################################

        self.doppler_shift_calc_0 = soniks.doppler.doppler_shift_calc(sat_name, c_rf, tle_p, s_lon, s_lat, s_alt, inv)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("trigger"), up)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.doppler_shift_calc_0, 'in'))
        self.msg_connect((self.doppler_shift_calc_0, 'out'), (self.analog_sig_source_x_0, 'cmd'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self, 0))
        self.connect((self, 0), (self.blocks_multiply_xx_0, 0))


    def get_c_rf(self):
        return self.c_rf

    def set_c_rf(self, c_rf):
        self.c_rf = c_rf

    def get_inv(self):
        return self.inv

    def set_inv(self, inv):
        self.inv = inv

    def get_s_alt(self):
        return self.s_alt

    def set_s_alt(self, s_alt):
        self.s_alt = s_alt

    def get_s_lat(self):
        return self.s_lat

    def set_s_lat(self, s_lat):
        self.s_lat = s_lat

    def get_s_lon(self):
        return self.s_lon

    def set_s_lon(self, s_lon):
        self.s_lon = s_lon

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_sat_name(self):
        return self.sat_name

    def set_sat_name(self, sat_name):
        self.sat_name = sat_name

    def get_tle_p(self):
        return self.tle_p

    def set_tle_p(self, tle_p):
        self.tle_p = tle_p

    def get_up(self):
        return self.up

    def set_up(self, up):
        self.up = up
        self.blocks_message_strobe_0.set_period(self.up)

