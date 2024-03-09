# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GEOSCAN Doppler shift compensation calculator
# GNU Radio version: 3.10.7.0

from gnuradio import gr
#import xmlrpc.client
import time
import datetime
from math import *
import ephem, pmt

class Tracker():

    def __init__(self, satellite, groundstation):
        self.groundstation = ephem.Observer()
        self.groundstation.lat = groundstation[0]
        self.groundstation.lon = groundstation[1]
        self.groundstation.elevation = int(groundstation[2])

        self.satellite = ephem.readtle(satellite["name"], satellite["tle1"], satellite["tle2"])

    def set_epoch(self, epoch=time.time()):

        self.groundstation.date = datetime.datetime.utcfromtimestamp(epoch)
        self.satellite.compute(self.groundstation)

    def doppler(self, frequency_hz):
        return -self.satellite.range_velocity / 299792458. * frequency_hz

    def tle_finder(filename, satname):
        with open(filename, 'r') as dat_file:
            data=dat_file.readlines()
            for num_line, line in enumerate(data):
                if satname in line:
                    break
            return data[num_line][:-1], data[num_line+1][:-1], data[num_line+2][:-1]

class doppler_shift_calc(gr.sync_block):
    """
    GEOSCAN Doppler shift compensation calculator
    """
    def __init__(self,satllite_name,center_freq,tle_path,lon,lat,alt,inv):
        gr.basic_block.__init__(
            self,
            name='Doppler shift compensation calculator',
            in_sig=[],
            out_sig=[])
        self.satllite_name=satllite_name
        self.tle_path=tle_path
        self.lon=lon
        self.lat=lat
        self.alt=alt
        self.center_freq=center_freq
        self.inv=inv
        name, tle1, tle2 = Tracker.tle_finder(filename=tle_path,satname=satllite_name)
        ec1_tle = { "name": name, \
                    "tle1": tle1, \
                    "tle2": tle2}
        station = (lat, lon, alt)
        self.tracker = Tracker(satellite=ec1_tle, groundstation=station)
        self.crxf=int(center_freq.replace('\n',''))
        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        
    def handle_msg(self, msg_pmt):
        if(msg_pmt):
            self.tracker.set_epoch(time.time())
            if(self.inv):
                self.message_port_pub(pmt.intern('out'), pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(-int(self.tracker.doppler(frequency_hz=self.crxf)))))
            else:
                self.message_port_pub(pmt.intern('out'), pmt.dict_add(pmt.make_dict(), pmt.intern("freq"), pmt.from_float(int(self.tracker.doppler(frequency_hz=self.crxf)))))