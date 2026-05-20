// SPDX-License-Identifier: CERN-OHL-S-2.0
// This public release is licensed under CERN-OHL-S-2.0.
// The copyright holder may also license the work separately under different terms.

`timescale 1ns / 1ps

module EFM#(parameter k=1024, parameter bits=12) (
    input clk,
    input rst,
    input signed [bits-1:0] x,
    output reg y
    );
    
    wire signed [bits:0] sum ;
    reg signed [bits:0] fbz ;

   assign sum = x + fbz;
      
    always@(posedge clk)
    begin
        if(rst) 
            begin
                fbz <=0;
                y   <=0;
            end
            
        else if (sum >=0) 
            begin
                y<=1'b1;
                fbz<=sum-k;
            end 
          
        else 
            begin
                y<=1'b0;
                fbz<=sum+k;
            end
     end
     
endmodule
