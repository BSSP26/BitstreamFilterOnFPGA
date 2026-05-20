// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module ATTENUATOR# (
parameter k     = 127,
parameter bits  = 7)(

input                        clk,
input                        rst,
input                        SELECT,
input       [bits-1:0]       GAIN,

output reg                   ATTENUATOR_OUT
);
    
wire signed [bits:0]   scaled_stream;
wire signed [bits+1:0] sum ;
reg  signed [bits+1:0] fbz ;

assign scaled_stream = SELECT ? GAIN : -GAIN;
assign sum = scaled_stream + fbz;
      
always@(posedge clk)
begin
    if(rst) 
        begin
        fbz             <=0;
        ATTENUATOR_OUT  <=0;
        end
            
    else if (sum >=0) 
        begin
        ATTENUATOR_OUT  <=1'b1;
        fbz             <=sum-k;
        end 
          
    else 
        begin
        ATTENUATOR_OUT  <=1'b0;
        fbz             <=sum+k;
        end
end
endmodule
