set terminal pdf dashed
set output "../Freepdk_Read_Access_time.pdf"
set palette color
set xlabel "Total Size (Kbit)"
set ylabel "Read Access time (ns)"
set key below
plot  'freepdk45_timing.dat' using ($1/1024):2 with line title '16-bit word' lt 0 lw 5 lc 0 ,\
 'freepdk45_timing.dat' using ($1/1024):2 with points title '' lt 0 lw 5 lc 0 ,\
 'freepdk45_timing.dat' using ($1/1024):3 with line title '32-bit word' lt 1 lw 5 lc 1 ,\
 'freepdk45_timing.dat' using ($1/1024):3 with points title '' lt 1 lw 5 lc 1 ,\
 'freepdk45_timing.dat' using ($1/1024):4 with line title '64-bit word' lt 2 lw 5 lc 2 ,\
 'freepdk45_timing.dat' using ($1/1024):4 with points title '' lt 2 lw 5 lc 2 ,\
 'freepdk45_timing.dat' using ($1/1024):5 with line title '128-bit word' lt 3 lw 5 lc 3 ,\
 'freepdk45_timing.dat' using ($1/1024):5 with points title '' lt 3 lw 5 lc 3 
