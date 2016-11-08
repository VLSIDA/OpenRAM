#!/usr/bin/gnuplot
#
# Demonstration of a common use scenario of the multiplot environment.
#
# AUTHOR: Hagen Wierstorf
#

reset

set terminal pdf dashed size 8cm,12cm
set output "Results.pdf"
set palette color

unset key

# Enable the use of macros
set macros

# MACROS
# Margins for each row resp. column
# top of top fig, bottom of top fig
TMARGIN = "set tmargin at screen 0.9; set bmargin at screen 0.575"
# top of lower fig, bottom of lower fig
BMARGIN = "set tmargin at screen 0.525; set bmargin at screen 0.15"
# left of left fig, right of left fig
LMARGIN = "set lmargin at screen 0.1; set rmargin at screen 0.48"
#  left point of right fig ,right most
RMARGIN = "set lmargin at screen 0.52; set rmargin at screen 0.9"

# Placement of the a,b,c,d labels in the graphs
POSA = "at graph 0.6,0.2 font ',5'"
POSB = "at graph 0.5,0.2 font ',5'"

### Start multiplot (2x2 layout)
set multiplot layout 4,1
# --- GRAPH a
set key outside center vertical top box 3
set lmargin at screen 0.2; set rmargin at screen 0.9
set tmargin at screen 0.88; set bmargin at screen 0.68
#@TMARGIN; @LMARGIN
#@NOXTICS; @YTICS
set label 1 '45nm Area' @POSA
set ylabel "mm^2"
plot  'density_data/freepdk45_size.dat' using ($1/1024):($2/1e6) with line axis x1y1 title '16-bit word size' lt 0 lw 5 lc 0 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($2/1e6) with points axis x1y1 title '' lt 0 lw 5 lc 0 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($3/1e6) with line axis x1y1 title '32-bit word size' lt 1 lw 5 lc 1 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($3/1e6) with points axis x1y1 title '' lt 1 lw 5 lc 1 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($4/1e6) with line axis x1y1 title '64-bit word size' lt 2 lw 5 lc 2 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($4/1e6) with points axis x1y1 title '' lt 2 lw 5 lc 2 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($5/1e6) with line axis x1y1 title '128-bit word size' lt 3 lw 5 lc 3 ,\
 'density_data/freepdk45_size.dat' using ($1/1024):($5/1e6) with points axis x1y1 title '' lt 3 lw 5 lc 3

# --- GRAPH b
unset key
set tmargin at screen 0.68; set bmargin at screen 0.48
#@TMARGIN; @RMARGIN
#@NOXTICS; @NOYTICS
set label 1 '180nm Area' @POSA
set ylabel "mm^2"
plot  'density_data/scn3me_size.dat' using ($1/1024):($2/1e6) with line axis x1y1 title '16-bit word size' lt 0 lw 5 lc 0 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($2/1e6) with points axis x1y1 title '' lt 0 lw 5 lc 0 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($3/1e6) with line axis x1y1 title '32-bit word size' lt 1 lw 5 lc 1 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($3/1e6) with points axis x1y1 title '' lt 1 lw 5 lc 1 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($4/1e6) with line axis x1y1 title '64-bit word size' lt 2 lw 5 lc 2 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($4/1e6) with points axis x1y1 title '' lt 2 lw 5 lc 2 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($5/1e6) with line axis x1y1 title '128-bit word size' lt 3 lw 5 lc 3 ,\
 'density_data/scn3me_size.dat' using ($1/1024):($5/1e6) with points axis x1y1 title '' lt 3 lw 5 lc 3
 
# --- GRAPH c
set tmargin at screen 0.48; set bmargin at screen 0.28
#@BMARGIN; @LMARGIN
#@XTICS; @YTICS
set label 1 '45nm Access time' @POSB
set ylabel "ns"
plot 'timing_data/freepdk45_timing.dat' using ($1/1024):2 with line axis x1y2 title '16-bit word' lt 0 lw 5 lc 0 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):2 with points axis x1y2 title '' lt 0 lw 5 lc 0 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):3 with line axis x1y2 title '32-bit word' lt 1 lw 5 lc 1 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):3 with points axis x1y2 title '' lt 1 lw 5 lc 1 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):4 with line axis x1y2 title '64-bit word' lt 2 lw 5 lc 2 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):4 with points axis x1y2 title '' lt 2 lw 5 lc 2 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):5 with line axis x1y2 title '128-bit word' lt 3 lw 5 lc 3 ,\
 'timing_data/freepdk45_timing.dat' using ($1/1024):5 with points axis x1y2 title '' lt 3 lw 5 lc 3 

# --- GRAPH d
set tmargin at screen 0.28; set bmargin at screen 0.08
#@BMARGIN; @RMARGIN
#@XTICS; @NOYTICS
set ylabel "ns"
set xlabel "Total Size (Kbits)"
set label 1 '180nm Access time' @POSB
plot 'timing_data/scn3me_timing.dat' using ($1/1024):2 with line axis x1y2 title '16-bit word' lt 0 lw 5 lc 0 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):2 with points axis x1y2 title '' lt 0 lw 5 lc 0 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):3 with line axis x1y2 title '32-bit word' lt 1 lw 5 lc 1 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):3 with points axis x1y2 title '' lt 1 lw 5 lc 1 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):4 with line axis x1y2 title '64-bit word' lt 2 lw 5 lc 2 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):4 with points axis x1y2 title '' lt 2 lw 5 lc 2 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):5 with line axis x1y2 title '128-bit word' lt 3 lw 5 lc 3 ,\
 'timing_data/scn3me_timing.dat' using ($1/1024):5 with points axis x1y2 title '' lt 3 lw 5 lc 3 
unset multiplot
### End multiplot
