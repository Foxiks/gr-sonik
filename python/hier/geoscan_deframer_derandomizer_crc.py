# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GEOSCAN UHF Link Deframer and Derandomizer (CRC)
# GNU Radio version: 3.10.7.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio import gr, pdu
import satellites.hier
import soniks.scramblers







class geoscan_deframer_derandomizer_crc(gr.hier_block2):
    def __init__(self, crc_state=True, packet_length=66, syncword='10010011000010110101000111011110', threshold=4):
        gr.hier_block2.__init__(
            self, "GEOSCAN UHF Link Deframer and Derandomizer (CRC)",
                gr.io_signature(1, 1, gr.sizeof_char*1),
                gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.crc_state = crc_state
        self.packet_length = packet_length
        self.syncword = syncword
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################

        self.satellites_sync_to_pdu_packed_0 = satellites.hier.sync_to_pdu_packed(
            packlen=packet_length,
            sync=syncword,
            threshold=threshold,
        )
        self.pdu_pdu_to_tagged_stream_1_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.geoscan_uhf_scrambler_0 = soniks.scramblers.geoscan_uhf_scrambler(crc_state)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(1)
        self.blocks_null_sink_1_0 = blocks.null_sink(gr.sizeof_char*1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.geoscan_uhf_scrambler_0, 'good'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.geoscan_uhf_scrambler_0, 'bad'), (self.pdu_pdu_to_tagged_stream_1_0, 'pdus'))
        self.msg_connect((self.satellites_sync_to_pdu_packed_0, 'out'), (self.geoscan_uhf_scrambler_0, 'in'))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.satellites_sync_to_pdu_packed_0, 0))
        self.connect((self, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_1_0, 0), (self.blocks_null_sink_1_0, 0))


    def get_crc_state(self):
        return self.crc_state

    def set_crc_state(self, crc_state):
        self.crc_state = crc_state

    def get_packet_length(self):
        return self.packet_length

    def set_packet_length(self, packet_length):
        self.packet_length = packet_length
        self.satellites_sync_to_pdu_packed_0.set_packlen(self.packet_length)

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

