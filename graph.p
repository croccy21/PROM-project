
set title "Access Times Graph"
set xtic auto
set ytics 0,1,2
set yrange [0:3]
set xlabel "time (hhmmss)"
set ylabel "0 = inactive , 1 = failed , 2 = sucess"
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 pi -1 ps 1.5
set pointintervalbox 2
set terminal jpeg
set output "AccessGraph.jpg" 
plot "data.dat" with linespoints ls 1
