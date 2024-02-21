# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Float (IQ) to Complex
# GNU Radio version: 3.10.7.0

from gnuradio import blocks
from gnuradio import gr







class float32IQ_to_complex(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Float (IQ) to Complex",
                gr.io_signature(1, 1, gr.sizeof_float*1),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Blocks
        ##################################################

        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_float*1, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self, 0))
        self.connect((self, 0), (self.blocks_deinterleave_0, 0))


