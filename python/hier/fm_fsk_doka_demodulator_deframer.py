# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM-FSK (DOKA) Demodulator and Deframer
# GNU Radio version: 3.10.7.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio import gr, pdu
import satellites.hier


class fm_fsk_doka_demodulator_deframer (gr.hier_block2):
    def __init__(self, baud_rate=4800, pack_len=132, samp_rate=48000, syncword="1100010010110010001010011000010101110000011011111011110001011010", taps=16, threshold=10):
        gr.hier_block2.__init__(
            self, "FM-FSK (DOKA) Demodulator+Deframer",
                gr.io_signature(1, 1, gr.sizeof_float*1),
                gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.baud_rate = baud_rate
        self.pack_len = pack_len
        self.samp_rate = samp_rate
        self.syncword = syncword
        self.taps = taps
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################

        self.satellites_sync_to_pdu_packed_0 = satellites.hier.sync_to_pdu_packed(
            packlen=pack_len,
            sync=syncword,
            threshold=threshold,
        )
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_fcc((int(samp_rate/baud_rate)), [taps], 0, samp_rate)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(1)
        self.blocks_float_to_uchar_1 = blocks.float_to_uchar()
        self.analog_rail_ff_1 = analog.rail_ff(0, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_sync_to_pdu_packed_0, 'out'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.analog_rail_ff_1, 0))
        self.connect((self.analog_rail_ff_1, 0), (self.blocks_float_to_uchar_1, 0))
        self.connect((self.blocks_float_to_uchar_1, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.satellites_sync_to_pdu_packed_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self, 0))


    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate

    def get_pack_len(self):
        return self.pack_len

    def set_pack_len(self, pack_len):
        self.pack_len = pack_len
        self.satellites_sync_to_pdu_packed_0.set_packlen(self.pack_len)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_syncword(self):
        return self.syncword

    def set_syncword(self, syncword):
        self.syncword = syncword
        self.satellites_sync_to_pdu_packed_0.set_sync(self.syncword)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.freq_xlating_fir_filter_xxx_1.set_taps([self.taps])

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.satellites_sync_to_pdu_packed_0.set_threshold(self.threshold)

