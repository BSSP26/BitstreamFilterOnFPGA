// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module BITSTREAM_FILTER(
input                         clk,
input                         rst,
input                         SIGNAL_INPUT,
input           [18:0]        alpha,
input           [6:0]         RESONANCE_GAIN,
input           [6:0]         INPUT_GAIN,

output                        TAP_1,
output                        TAP_2,
output                        TAP_3,
output                        TAP_4);


///Internal Signals
wire                    RESONANCE_ATTEN;
wire                    INPUT_ATTEN;


//ATTENUABLE PARAMETER/////////////////////////////////////////////
ATTENUATOR ATTENUATOR_INPUT_GAIN(
.clk(clk),
.rst(rst),
.SELECT(SIGNAL_INPUT),
.GAIN(INPUT_GAIN),
.ATTENUATOR_OUT(INPUT_ATTEN));

ATTENUATOR ATTENUATOR_RESONANCE_GAIN(
.clk(clk),
.rst(rst),
.SELECT(TAP_4),
.GAIN(RESONANCE_GAIN),
.ATTENUATOR_OUT(RESONANCE_ATTEN));


//FILTER STRUCTURE///////////////////////////////////////////////////
FILTER_STAGE_EXTENDED STAGE_1(
.clk(clk),
.rst(rst),
.SIGNAL_INPUT(INPUT_ATTEN),
.RESONANCE(RESONANCE_ATTEN),
.alpha(alpha),
.STREAM_OUT(TAP_1)); 

FILTER_STAGE STAGE_2(
.clk(clk),
.rst(rst),
.SIGNAL_INPUT(TAP_1),
.alpha(alpha),
.STREAM_OUT(TAP_2));

FILTER_STAGE STAGE_3(
.clk(clk),
.rst(rst),
.SIGNAL_INPUT(TAP_2),
.alpha(alpha),
.STREAM_OUT(TAP_3));

FILTER_STAGE STAGE_4(
.clk(clk),
.rst(rst),
.SIGNAL_INPUT(TAP_3),
.alpha(alpha),
.STREAM_OUT(TAP_4));


endmodule
