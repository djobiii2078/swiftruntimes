#!/usr/bin/gnuplot
# Output a png called barchart.png. You
# could instead leave out the output filename
# here and redirect the output to a file
# like ./myconfig.gnu > barchart.png.set terminal pngset output "barchart.png"
set terminal pdfcairo enhanced font "Inter"
set output "mergelist.pdf"

# Empty boxes is the default. Fill them in.
set style fill solid
# By default, adjacent boxes are extended
# in width until they touch each other. I
# want to fit two bars side by side at each
# point, and leave a little space after that, so
# I'm making the bars 0.4 units wide. (Two
# bars at 0.4 each leaves 0.2 units for space.)
set boxwidth 0.4

# Labels!
#set title "A Fancy Bar Chart"
set ylabel "Merge time (ns)"
set xlabel "Number of vCPUs"

set style line 2 lc rgb 'black' lt 1 lw 1
#set style data histogram
set style histogram cluster gap 2
set key left top 
set style fill pattern border -1
set boxwidth 0.9
set grid ytics

set style arrow 5 heads filled size screen 0.03,15,135 ls 1

# Rotate the labels on the x axis. Saves space
# and looks nice.
#set xtics rotate

# Kind of hacky, but I want exactly the years in
# my file (2000 to 2006) with a tiny bit of space
# on either side.
#set xrange [1999.5:2006.9]

# The y axis starts at zero and ends at 350.
#set yrange [0:350]

# I like grids on graphs; it makes it easier to read.
set style line 81 lt 0 lc rgb "#808080" lw 0.5

set grid xtics
set grid ytics
set grid mxtics
set grid mytics

# Put the grid behind anything drawn and use the linestyle 81
set grid back ls 81
# Now read the data from numbers.dat and plot
# the graph. 'using' takes two values: the
# position on the x axis, the position on the y
# axis. "using 1:2" means the position on the x
# axis comes from the first column in
# numbers.dat and the position on the y axis
# comes from the second column. "using 1:3"
# instead sets the y axis based on the third
# column. And so on.


set arrow from 9.5,150 to 9.5,850 heads ls 2
set label "9.9 x" at 8.7,500 textcolor linetype 1

# First value: use the 2nd column and draw red
# (#00FF00) boxes. Second value: use the 3rd
# column and draw green (#00FF00) boxes. But
# move the x axis over a bit.

plot "unpause.txt" using ($2*1000):xtic(1) title "naive" w lp ls 2 lt 2 ps 1.1 lw 2, \
	"unpause.txt" using ($3*1000) title "ppsm" w lp ls 2 ps 1.1 lw 2 lt 4

# See the ($1+0.4) on that second one? If you're
# drawing two boxes at the same x coordinate,
# they're going to be on top of each other.
# Maybe not what you want, so this shifts the
# second box along on the x axis. The boxes
# are 0.4 units wide (the boxwidth above!), so
# moving that much makes them side by side.
