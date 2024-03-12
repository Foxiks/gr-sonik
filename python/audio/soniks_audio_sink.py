# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Soniks audio sink
# GNU Radio version: 3.10.7.0

import wave, struct,io
from pydub import AudioSegment
import numpy
from gnuradio import gr


class soniks_audio_sink(gr.sync_block):
    """Soniks audio sink"""

    def __init__(self, samp_rate="48000", path='/home/user/', bitrate="192k"):
        gr.sync_block.__init__(
            self,
            name='Soniks Audio Sink',
            in_sig=[numpy.float32],
            out_sig=None)

        self.audio_samples_array=bytearray()
        self.samp_rate=samp_rate
        self.path=path
        self.bitrate=bitrate
        self.output_format=str(path.split('.')[-1]).lower()
    
    def __del__(self):
        wav_buf=io.BytesIO()
        if(self.output_format=="wav"):
            with wave.open(self.path, "wb") as out_f:
                out_f.setnchannels(1)
                out_f.setsampwidth(4) # number of bytes
                out_f.setframerate(int(self.samp_rate))
                out_f.writeframesraw(bytes(self.audio_samples_array))
        else:
            with wave.open(wav_buf, "wb") as out_f:
                out_f.setnchannels(1)
                out_f.setsampwidth(4) # number of bytes
                out_f.setframerate(int(self.samp_rate))
                out_f.writeframesraw(bytes(self.audio_samples_array))
            audio = AudioSegment.from_file(wav_buf, format="wav")
            audio.export(self.path, format=self.output_format, parameters=["-b:a", self.bitrate, "-ar", self.samp_rate])

    def work(self, input_items, output_items):
        msg_out=input_items[0][:]
        for i in range(len(msg_out)):
            self.audio_samples_array.extend(bytearray(struct.pack("f", msg_out[i])) )
        return len(input_items[0])