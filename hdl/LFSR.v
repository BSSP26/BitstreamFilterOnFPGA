// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module LFSR(
input                   clk,
input                   rst,
output                  LFSR_STREAM);

parameter MAX_COUNTER = 268435456;

reg     [31:0]   r_LFSR;
reg              r_XNOR;
reg     [31:0]   counter;

always @(*)
begin
r_XNOR = r_LFSR[31] ^~ r_LFSR[21] ^~ r_LFSR[1] ^~ r_LFSR[0];
end

wire [31:0] clk_scaler;
assign clk_scaler       = 4294967;

always @(posedge clk) begin
    if (rst) begin
        counter <= 0;
        r_LFSR  <= 0;
    end else if (counter >= MAX_COUNTER) begin
        counter <= 0;
        r_LFSR  <= {r_LFSR[30:0], r_XNOR};
    end else begin
        counter <= counter + clk_scaler;
    end
end

assign LFSR_STREAM = r_LFSR[0];
endmodule
