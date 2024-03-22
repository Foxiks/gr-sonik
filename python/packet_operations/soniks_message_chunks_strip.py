# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks Messages Multiplyer (PDU)
# GNU Radio version: 3.10.7.0

from gnuradio import gr
import pmt
    
class soniks_message_chunks_strip(gr.sync_block):
    """
    Frames add
    """
    def __init__(self, chunk_len):
        gr.basic_block.__init__(
            self,
            name='Soniks Message Chunks Strip',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg1)
        self.chunk_len=chunk_len

    def handle_msg1(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        msg_o = pmt.u8vector_elements(msg)
        if((len(msg_o)/self.chunk_len).is_integer()):
            for i in range(0,len(msg_o),self.chunk_len):
                msg1=msg_o[i:i+self.chunk_len]
                msg_out = pmt.init_u8vector(len(msg1), msg1)
                msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
                self.message_port_pub(pmt.intern('out'), msg_out)
        else:
            print("(len(pdu)/self.chunk_len).is_integer() = False!")