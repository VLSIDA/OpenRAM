set terminal pdf dashed
set output "../Freepdk_Area.pdf"
set palette color
set xlabel "Total Size (Kbit)"
set ylabel "Area (mm^2)"
set key below
plot  'freepdk45_size.dat' using ($1/1024):($2/1e6) with line title '16-bit word' lt 0 lw 5 lc 0 ,\
 'freepdk45_size.dat' using ($1/1024):($2/1e6) with points title '' lt 0 lw 5 lc 0 ,\
 'freepdk45_size.dat' using ($1/1024):($3/1e6) with line title '32-bit word' lt 1 lw 5 lc 1 ,\
 'freepdk45_size.dat' using ($1/1024):($3/1e6) with points title '' lt 1 lw 5 lc 1 ,\
 'freepdk45_size.dat' using ($1/1024):($4/1e6) with line title '64-bit word' lt 2 lw 5 lc 2 ,\
 'freepdk45_size.dat' using ($1/1024):($4/1e6) with points title '' lt 2 lw 5 lc 2 ,\
 'freepdk45_size.dat' using ($1/1024):($5/1e6) with line title '128-bit word' lt 3 lw 5 lc 3 ,\
 'freepdk45_size.dat' using ($1/1024):($5/1e6) with points title '' lt 3 lw 5 lc 3 
