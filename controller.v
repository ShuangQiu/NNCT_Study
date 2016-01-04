
module controller ( clk, rst, load, m );
output [2:0] load;
output [4:0] m;
input  clk, rst;
    wire \ps[1] , \ps[0] , \m[4] , \m[3] , \ns[1] , n30, n31, n32, n33, n34, 
        n35;
    assign load[0] = \m[3] ;
    assign m[4] = \m[4] ;
    assign m[3] = \m[3] ;
    assign m[2] = \m[4] ;
    assign m[1] = \m[3] ;
    NR2 U14 ( .A(rst), .B(n32), .Z(\ns[1] ) );
    AN3 U15 ( .A(n33), .B(n31), .C(\ps[0] ), .Z(m[0]) );
    AN3 U16 ( .A(n32), .B(n33), .C(n34), .Z(load[1]) );
    AO2 U17 ( .A(n31), .B(\ps[0] ), .C(\ps[1] ), .D(n30), .Z(n32) );
    ND2 U18 ( .A(\ps[0] ), .B(\ps[1] ), .Z(n34) );
    ND2 U19 ( .A(n33), .B(n30), .Z(n35) );
    NR2 U20 ( .A(n34), .B(rst), .Z(\m[4] ) );
    NR2 U21 ( .A(n35), .B(n31), .Z(\m[3] ) );
    IV U22 ( .A(rst), .Z(n33) );
    IV U23 ( .A(n35), .Z(load[2]) );
    FD1 \ps_reg[0]  ( .D(load[2]), .CP(clk), .Q(\ps[0] ), .QN(n30) );
    FD1 \ps_reg[1]  ( .D(\ns[1] ), .CP(clk), .Q(\ps[1] ), .QN(n31) );
endmodule

