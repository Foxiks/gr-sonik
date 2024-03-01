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
from random import randint

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
        #out = output_items[0]
        output_items = numpy.array([0], dtype=numpy.uint8)
        # <+signal processing here+>
        # <+ --- +>
        for _ in range(512-len(output_items)):
            output_items= numpy.append(output_items, 0)
        for i in range(16):
            output_items[i] = 0xAA
        for k in range(16,512,1):
            output_items[k] = randint(1,255)
        return len([output_items][0])