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
import os

class soniks_data_sink(gr.sync_block):
    """
    Soniks Network Data Sink
    """
    def __init__(self,decoded_data_file_path="/tmp/.satnogs/data/", sat_id="0",packet_len=132):
        gr.sync_block.__init__(self,
            name="Soniks Network Frames Sink",
            in_sig=[numpy.ubyte],
            out_sig=[numpy.ubyte])
        
        self.decoded_data_file_path=decoded_data_file_path
        self.sat_id=sat_id
        self.packet_len=packet_len
        self.x=0
        self.pre_x=0
        self.old_pre_x=0
        self.out_frame_temp_arr=[]

        if(not os.path.exists(f"{decoded_data_file_path}")):
            os.system(f"mkdir -p {decoded_data_file_path}")


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        for i in range(len(in0)):
            self.out_frame_temp_arr.append(in0[i])
        if(len(self.out_frame_temp_arr)==self.packet_len):
            self.pre_x=time.mktime(datetime.datetime.now().timetuple())
            if(self.pre_x>self.old_pre_x):
                self.x=0
            else:
                self.x+=1
            time_st=datetime.datetime.now().strftime(f"%Y-%m-%dT%H-%M-%S")
            with open(f"{self.decoded_data_file_path}data_{self.sat_id}_{time_st}_g{self.x}",'wb') as out1:
                out1.write(int(''.join([hex(self.out_frame_temp_arr[i])[2:].zfill(2) for i in range(len(self.out_frame_temp_arr))]), 16).to_bytes(self.packet_len,'big'))
            self.out_frame_temp_arr.clear()
            self.old_pre_x=self.pre_x
        elif(len(self.out_frame_temp_arr)>self.packet_len):
            self.pre_x=time.mktime(datetime.datetime.now().timetuple())
            if(self.pre_x>self.old_pre_x):
                self.x=0
            else:
                self.x+=1
            time_st=datetime.datetime.now().strftime(f"%Y-%m-%dT%H-%M-%S")
            with open(f"{self.decoded_data_file_path}data_{self.sat_id}_{time_st}_g{self.x}",'wb') as out1:
                out1.write(int(''.join([hex(self.out_frame_temp_arr[i])[2:].zfill(2) for i in range(self.packet_len)]), 16).to_bytes(self.packet_len,'big'))
            self.out_frame_temp_arr=self.out_frame_temp_arr[self.packet_len:]
            self.old_pre_x=self.pre_x
        else:
            pass
        # <+ --- +>
        
        out[:] = in0
        return len(output_items[0])