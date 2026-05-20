// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module STSE_EXTENDED#(
parameter WIDTH = 16)(
input                                clk,
input                                rst,
input                                select_1,
input                                select_2,
input                                select_3,
input       signed  [WIDTH-1:0]      in_1,

output  reg signed  [WIDTH-1:0]      out);


always@(posedge clk)
begin
if (rst)        out <= 0;
else if (!select_1  &&  !select_2    &&   !select_3)     out <=  (in_1 <<< 2);
else if (!select_1  &&  !select_2    &&    select_3)     out <= -(in_1 <<< 2);
else if (!select_1  &&   select_2    &&   !select_3)     out <=  (in_1 <<< 1);
else if (!select_1  &&   select_2    &&    select_3)     out <= -((in_1 <<< 2) + (in_1 <<< 1));
else if ( select_1  &&  !select_2    &&   !select_3)     out <=  ((in_1 <<< 2) + (in_1 <<< 1));
else if ( select_1  &&  !select_2    &&    select_3)     out <= -(in_1 <<< 1);
else if ( select_1  &&   select_2    &&   !select_3)     out <=  (in_1 <<< 2);
else if ( select_1  &&   select_2    &&    select_3)     out <= -(in_1 <<< 2);
else                                                     out <= 0;
end

endmodule
