// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module FILTER_STAGE(
input               clk,
input               rst,
input               SIGNAL_INPUT,
input   [18:0]      alpha,

output              STREAM_OUT);


wire signed     [20:0]  alpha_gs;
wire signed     [25:0]  ACCU_OUT;
    


//Bitstream Adder
STSE #(
.WIDTH(21))
STSE_FILTER_STAGE(
.clk(clk),
.rst(rst),
.select_1(SIGNAL_INPUT),
.select_2(STREAM_OUT),
.in_1(alpha),
.out(alpha_gs)); 

//Integration
ACCU #(
.IN_WIDTH(21),
.SIZE(26))
ACCU_FILTER_STAGE(
.clk(clk),
.rst(rst),
.IN(alpha_gs),
.ACCU_OUT(ACCU_OUT));

//DIVIDE Integrator
EFM #(.k(19098593), .bits(26))
EFM_FILTER_STAGE(
.clk(clk),
.rst(rst),
.x(ACCU_OUT),
.y(STREAM_OUT)); 

endmodule
