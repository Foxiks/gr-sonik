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
import time, pmt
from random import randint

class binary_debug(gr.sync_block):
    """
    Debug
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Soniks Network Frames Sink",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8])

    '''def work(self, input_items, output_items):
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
        return len([output_items][0])'''

    def work(self, input_items, output_items):
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key) # convert from PMT to python string
            value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
            print('key:', key)
            print('value:', value, type(value))
            print('')
        return len(input_items[0])