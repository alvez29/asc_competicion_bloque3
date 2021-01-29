mkdir $1
mkdir $1/imagenes
mv *.out $1
cat > $1/scriptgnuplot.p << EOF
set terminal png size 1000,500 
set output 'plot_seed_00.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed00.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_01.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed01.out' with points pt 7 lt -1 
set terminal png size 1000,500

set output 'plot_seed_02.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed02.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_03.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed03.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_04.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed04.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_05.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed05.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_06.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed06.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_07.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed07.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_08.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed08.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_09.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed09.out' with points pt 7 lt -1 

set terminal png size 1000,500
set output 'plot_seed_099.png'
plot [0:1] 'PF.dat' using 1:2 with points pt 7 lt 1, '$2_seed099.out' with points pt 7 lt -1 
EOF
cp $3 $1
mv $1/$3 $1/PF.dat  
cd $1
gnuplot scriptgnuplot.p
mv *.png ./imagenes/


