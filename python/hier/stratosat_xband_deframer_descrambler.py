# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Stratosat TK-1 X-Band Deframer and Descrambler
# GNU Radio version: 3.10.7.0

from gnuradio import gr
from gnuradio import gr, pdu, blocks
import satellites.hier
import soniks.scramblers







class stratosat_xband_deframer_descrambler(gr.hier_block2):
    def __init__(self, frame_len=130, syncword="00000000000000001111011010001101", threshold=3):
        gr.hier_block2.__init__(
            self, "Stratosat TK-1 X-Band Deframer and Descrambler",
                gr.io_signature(1, 1, gr.sizeof_char*1),
                gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.frame_len = frame_len
        self.syncword = syncword
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################
        self.blocks_pack_k_bits_bb_1 = blocks.pack_k_bits_bb(1)
        self.stratosat_xband_scrambler_0 = soniks.scramblers.stratosat_xband_scrambler()
        self.satellites_sync_to_pdu_packed_0 = satellites.hier.sync_to_pdu_packed(
            packlen=frame_len,
            sync=syncword,
            threshold=threshold,
        )
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')


        ##################################################
        # Connections
        ##################################################
        
        self.msg_connect((self.satellites_sync_to_pdu_packed_0, 'out'), (self.stratosat_xband_scrambler_0, 'in'))
        self.msg_connect((self.stratosat_xband_scrambler_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.connect((self, 0), (self.blocks_pack_k_bits_bb_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_1, 0), (self.satellites_sync_to_pdu_packed_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self, 0))


    def get_frame_len(self):
        return self.frame_len

    def set_frame_len(self, frame_len):
        self.frame_len = frame_len
        self.satellites_sync_to_pdu_packed_0.set_packlen(self.frame_len)

    def get_syncword(self):
        return self.syncword

    def set_syncword(self, syncword):
        self.syncword = syncword
        self.satellites_sync_to_pdu_packed_0.set_sync(self.syncword)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.satellites_sync_to_pdu_packed_0.set_threshold(self.threshold)

