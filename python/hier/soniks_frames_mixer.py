# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks Frames Multiplyer
# GNU Radio version: 3.10.7.0

from gnuradio import gr
from gnuradio import gr, pdu
import soniks.packet_operations







class soniks_frames_mixer(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Soniks Frames Mixer",
                gr.io_signature.makev(2, 2, [gr.sizeof_char*1, gr.sizeof_char*1]),
                gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Blocks
        ##################################################

        self.soniks_messages_multiplyer_pdu_0 = soniks.packet_operations.soniks_messages_mixer_pdu()
        self.pdu_tagged_stream_to_pdu_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.soniks_messages_multiplyer_pdu_0, 'in 1'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0, 'pdus'), (self.soniks_messages_multiplyer_pdu_0, 'in 0'))
        self.msg_connect((self.soniks_messages_multiplyer_pdu_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self, 1), (self.pdu_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self, 0))


