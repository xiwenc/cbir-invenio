# set terminal png transparent nocrop enhanced size 450,500 font "arial,8"
# set output 'recall.png'
set terminal epslatex size 4.5,5.2 standalone color colortext 10
set output 'out.tex'

set boxwidth 0.9 absolute
set style fill   solid 1.00 border lt -1
set key inside right top vertical Right noreverse noenhanced autotitle nobox
set style histogram clustered gap 1 title textcolor lt -1
set datafile missing '-'
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -90
set xtics  norangelimit
set xtics   ()
set title "Precision"
set yrange [ 0.00000 : 2.0 ] noreverse nowriteback
plot 'build/precision.dat' using 2:xtic(1) ti col, '' u 3 ti col, '' u 4 ti col, '' u 5 ti col
