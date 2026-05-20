// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module ACCU#(
    parameter signed LIMIT = 26'sd19098593,
    parameter IN_WIDTH = 15,
    parameter SIZE     = 26
    )(
    input clk,
    input rst,
    input signed [IN_WIDTH-1:0] IN,
    output signed [SIZE-1:0] ACCU_OUT
);
    reg  signed [SIZE-1:0]  ACCU_Z;    
    wire signed [SIZE:0]    next_accu = ACCU_Z + IN;

    
    assign ACCU_OUT =   (next_accu > LIMIT) ?   LIMIT  :
                        (next_accu < -LIMIT)?   -LIMIT :
                                                next_accu;

    always @(posedge clk) begin
        if (rst)
            ACCU_Z <= 0;
        else
            ACCU_Z <= ACCU_OUT ;
    end
endmodule
