# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GEOSCAN UHF Link Descrambler (CRC)
# GNU Radio version: 3.10.7.0

from gnuradio import gr
import pmt
from crc import Calculator, Configuration
    
class geoscan_uhf_scrambler(gr.sync_block):
    """
    GEOSCAN UHF Link Descrambler (CRC)
    """
    def __init__(self,crc_selector):
        gr.basic_block.__init__(
            self,
            name='GEOSCAN UHF Link Descrambler (CRC)',
            in_sig=[],
            out_sig=[])
        self.calculator = Calculator(geoscan_uhf_scrambler.crc_calc_param())
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('good'))
        self.message_port_register_out(pmt.intern('bad'))
        self.mask=[0xFF, 0xE1, 0x1D, 0x9A, 0xED, 0x85, 0x33, 0x24, 
                   0xEA, 0x7A, 0xD2, 0x39, 0x70, 0x97, 0x57, 0x0A, 
                   0x54, 0x7D, 0x2D, 0xD8, 0x6D, 0x0D, 0xBA, 0x8F, 
                   0x67, 0x59, 0xC7, 0xA2, 0xBF, 0x34, 0xCA, 0x18, 
                   0x30, 0x53, 0x93, 0xDF, 0x92, 0xEC, 0xA7, 0x15, 
                   0x8A, 0xDC, 0xF4, 0x86, 0x55, 0x4E, 0x18, 0x21, 
                   0x40, 0xC4, 0xC4, 0xD5, 0xC6, 0x91, 0x8A, 0xCD, 
                   0xE7, 0xD1, 0x4E, 0x09, 0x32, 0x17, 0xDF, 0x83, 
                   0xFF, 0xF0]
        self.crc_selector=crc_selector

    def crc_calc_param():
        config = Configuration(
            width=16,
            polynomial=0x8005,
            init_value=0xffff,
            final_xor_value=0x0000,
            reverse_input=False,
            reverse_output=False,
        )
        return config

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        arr=[]
        msg = pmt.u8vector_elements(msg)
        for i in range(len(msg)):
            try:
                arr.append(msg[i]^self.mask[i])
            except IndexError:
                arr.append(msg[i])
        msg_out = arr
        if(self.crc_selector):
            crc_calculated=self.calculator.checksum(bytes(arr[:64]))
            crc_frame_stamp=int.from_bytes(bytes(arr[64:]),'big')
            if(crc_calculated==crc_frame_stamp):
                msg_out = pmt.init_u8vector(len(msg_out), msg_out)
                msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
                self.message_port_pub(pmt.intern('good'), msg_out)
            else:
                msg_out = pmt.init_u8vector(len(msg_out), msg_out)
                msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
                self.message_port_pub(pmt.intern('bad'), msg_out)
        else:
            msg_out = pmt.init_u8vector(len(msg_out), msg_out)
            msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
            self.message_port_pub(pmt.intern('good'), msg_out)