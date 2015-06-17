# set terminal png transparent nocrop enhanced size 450,500 font "arial,8"
# set output 'recall.png'
set terminal postscript eps enhanced size 5,3 color colortext 10
set output outfile

set boxwidth 1 absolute
set style fill solid 1.00 border lt -1
set key inside right top vertical Right noreverse noenhanced autotitle nobox
set style histogram clustered gap 1 title textcolor lt -1
set datafile missing '-'
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -90 autojustify
set xtics  norangelimit
set xtics   ()
set auto y
plot infile using 2:xtic(1) ti col, '' u (-$3) ti col
