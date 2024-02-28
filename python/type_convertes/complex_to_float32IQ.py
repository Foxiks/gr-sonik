# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Complex to Float (IQ)
# GNU Radio version: 3.10.7.0

from gnuradio import blocks
from gnuradio import gr







class complex_to_float32IQ(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Complex to Float (IQ)",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_float*1),
        )

        ##################################################
        # Blocks
        ##################################################

        self.blocks_interleave_0 = blocks.interleave(gr.sizeof_float*1, 1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_interleave_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_interleave_0, 0))
        self.connect((self.blocks_interleave_0, 0), (self, 0))
        self.connect((self, 0), (self.blocks_complex_to_float_0, 0))


