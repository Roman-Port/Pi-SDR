#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Pisdr Mode Broadfm
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import rds
import wx


class pisdr_mode_broadfm(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Pisdr Mode Broadfm")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 250000
        self.if_samp_rate = if_samp_rate = samp_rate
        self.pll_min_freq = pll_min_freq = 18950*2*3.14159/if_samp_rate
        self.pll_max_freq = pll_max_freq = 19050*2*3.14159/if_samp_rate
        self.output_audio_samp_rate = output_audio_samp_rate = 50000
        self.fm_freq = fm_freq = 104.1

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(2, firdes.root_raised_cosine(
        	1, 19000, 2375, 1, 100))
        self.rational_resampler_xxx_0_0_0_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  19000/250e3,
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)

        self.low_pass_filter_0_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, if_samp_rate, 15000, 2000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, if_samp_rate, 15000, 2000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 80000, 10000, firdes.WIN_HAMMING, 6.76))
        self.gr_rds_parser_0 = rds.parser(False, False, 1)
        self.gr_rds_decoder_0 = rds.decoder(False, False)
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_fcc(1, (firdes.low_pass(2500.0,250000,2.6e3,2e3,firdes.WIN_HAMMING)), 57e3, 250000)
        self.digital_psk_demod_0 = digital.psk.psk_demod(
          constellation_points=2,
          differential=False,
          samples_per_symbol=4,
          excess_bw=0.35,
          phase_bw=6.28/100.0,
          timing_bw=6.28/100.0,
          mod_code="gray",
          verbose=False,
          log=False,
          )
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('E:\\test_recording.wav', True)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('E:\\test.wav', 2, 50000, 16)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_char*1, 2)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'E:\\test_rds', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 3)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	2, if_samp_rate, 35000, 41000, 1000, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	1, if_samp_rate, 17000, 21000, 1000, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(output_audio_samp_rate, '', True)
        self.analog_pll_refout_cc_0_0 = analog.pll_refout_cc(0.0002, pll_max_freq, pll_min_freq)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=samp_rate,
        	audio_decim=1,
        	deviation=75000,
        	audio_pass=90000,
        	audio_stop=94000,
        	gain=1.0,
        	tau=0,
        )
        self.analog_fm_deemph_1 = analog.fm_deemph(fs=if_samp_rate, tau=75e-6)
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=if_samp_rate, tau=75e-6)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gr_rds_decoder_0, 'out'), (self.gr_rds_parser_0, 'in'))
        self.connect((self.analog_fm_deemph_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.analog_fm_deemph_1, 0), (self.rational_resampler_xxx_0_0_0_0, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.analog_pll_refout_cc_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_pll_refout_cc_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.analog_pll_refout_cc_0_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.analog_fm_deemph_1, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.gr_rds_decoder_0, 0))
        self.connect((self.digital_psk_demod_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.audio_sink_0, 1))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_wavfile_sink_0, 1))
        self.connect((self.rational_resampler_xxx_0_0_0_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_psk_demod_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_if_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 80000, 10000, firdes.WIN_HAMMING, 6.76))

    def get_if_samp_rate(self):
        return self.if_samp_rate

    def set_if_samp_rate(self, if_samp_rate):
        self.if_samp_rate = if_samp_rate
        self.set_pll_min_freq(18950*2*3.14159/self.if_samp_rate)
        self.set_pll_max_freq(19050*2*3.14159/self.if_samp_rate)
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.if_samp_rate, 15000, 2000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.if_samp_rate, 15000, 2000, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(2, self.if_samp_rate, 35000, 41000, 1000, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.if_samp_rate, 17000, 21000, 1000, firdes.WIN_HAMMING, 6.76))

    def get_pll_min_freq(self):
        return self.pll_min_freq

    def set_pll_min_freq(self, pll_min_freq):
        self.pll_min_freq = pll_min_freq
        self.analog_pll_refout_cc_0_0.set_min_freq(self.pll_min_freq)

    def get_pll_max_freq(self):
        return self.pll_max_freq

    def set_pll_max_freq(self, pll_max_freq):
        self.pll_max_freq = pll_max_freq
        self.analog_pll_refout_cc_0_0.set_max_freq(self.pll_max_freq)

    def get_output_audio_samp_rate(self):
        return self.output_audio_samp_rate

    def set_output_audio_samp_rate(self, output_audio_samp_rate):
        self.output_audio_samp_rate = output_audio_samp_rate

    def get_fm_freq(self):
        return self.fm_freq

    def set_fm_freq(self, fm_freq):
        self.fm_freq = fm_freq


def main(top_block_cls=pisdr_mode_broadfm, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
