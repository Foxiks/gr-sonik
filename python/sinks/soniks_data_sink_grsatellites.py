# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks Data Sink (Gr-Satellites)
# GNU Radio version: 3.10.7.0

from gnuradio import gr
import datetime
import time
import os, pmt

class soniks_data_sink_grsatellites(gr.sync_block):
    """
    Soniks Network Data Sink (Gr-Satellites)
    """
    def __init__(self,decoded_data_file_path="/tmp/.satnogs/data/", sat_id="0"):
        gr.sync_block.__init__(self,
            name="Soniks Network Frames Sink (Gr-Satellites)",
            in_sig=[],
            out_sig=None)
        
        self.decoded_data_file_path=decoded_data_file_path
        self.sat_id=sat_id
        self.x=0
        self.pre_x=0
        self.old_pre_x=0
        self.out_frame_temp_arr=[]

        if(not os.path.exists(f"{decoded_data_file_path}")):
            os.system(f"mkdir -p {decoded_data_file_path}")

        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        msg_out = pmt.u8vector_elements(msg)
        for i in range(len(msg_out)):
            self.out_frame_temp_arr.append(msg_out[i])

        self.pre_x=time.mktime(datetime.datetime.now().timetuple())
        if(self.pre_x>self.old_pre_x):
            self.x=0
        else:
            self.x+=1
        time_st=datetime.datetime.now().strftime(f"%Y-%m-%dT%H-%M-%S")
        with open(f"{self.decoded_data_file_path}data_{self.sat_id}_{time_st}_g{self.x}",'wb') as out1:
            out1.write(int(''.join([hex(self.out_frame_temp_arr[i])[2:].zfill(2) for i in range(len(self.out_frame_temp_arr))]), 16).to_bytes(len(msg_out),'big'))
        self.out_frame_temp_arr.clear()
        self.old_pre_x=self.pre_x