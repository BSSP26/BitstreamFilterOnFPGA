// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps


module TOP(
input                       clk,
input                       rst, 
output                      PMOD_DIRECT_STREAM,
output                      FILTER_OUT);

// Static AE / measurement configuration
// fc = 440 Hz for fres ~= 0.1 Hz -> alpha ~= 4400
localparam [18:0] ALPHA             = 19'd4400;
localparam [6:0]  RESONANCE_GAIN    = 7'd0;
localparam [6:0]  INPUT_GAIN        = 7'd127;


assign PMOD_DIRECT_STREAM = FILTER_OUT;
wire   LFSR_STREAM;

LFSR LFSR_192kHz(
.clk(clk),
.rst(rst),
.LFSR_STREAM(LFSR_STREAM));

/////FILTER
BITSTREAM_FILTER LADDER_CASCADE(
.clk(clk),
.rst(rst),
.SIGNAL_INPUT(LFSR_STREAM),
.alpha(ALPHA),
.RESONANCE_GAIN(RESONANCE_GAIN),
.INPUT_GAIN(INPUT_GAIN),

.TAP_1(),
.TAP_2(),
.TAP_3(),
.TAP_4(FILTER_OUT));   
  
endmodule
