# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks Data Sink
# GNU Radio version: 3.10.7.0

import numpy
from gnuradio import gr
import datetime
import time

class binary_debug(gr.sync_block):
    """
    Debug
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Soniks Network Frames Sink",
            in_sig=[numpy.ubyte],
            out_sig=[numpy.ubyte])

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        print(type(in0))
        # <+ --- +>
        
        out[:] = in0
        return len(output_items[0])