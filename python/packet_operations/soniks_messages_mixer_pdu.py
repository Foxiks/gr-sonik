# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks Messages Multiplyer (PDU)
# GNU Radio version: 3.10.7.0

from gnuradio import gr
import pmt
    
class soniks_messages_mixer_pdu(gr.sync_block):
    """
    Frames add
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='Soniks Messages Mixer (PDU)',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in 0'))
        self.message_port_register_in(pmt.intern('in 1'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in 0'), self.handle_msg1)
        self.set_msg_handler(pmt.intern('in 1'), self.handle_msg2)

    def handle_msg1(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        msg_out = pmt.u8vector_elements(msg)
        msg_out = pmt.init_u8vector(len(msg_out), msg_out)
        msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
        self.message_port_pub(pmt.intern('out'), msg_out)
    
    def handle_msg2(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        msg_out = pmt.u8vector_elements(msg)
        msg_out = pmt.init_u8vector(len(msg_out), msg_out)
        msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
        self.message_port_pub(pmt.intern('out'), msg_out)