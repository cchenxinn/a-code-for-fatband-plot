cp PROCAR_back PROCAR
mkdir -p tmpfd
num_ion=`cat PROCAR |awk NR==2'{print $12}'`
num_bnd=`cat PROCAR |awk NR==2'{print $8}'`
num_kpt=`cat PROCAR |awk NR==2'{print $4}'`
num_tkn=`expr $num_bnd \* $(($num_ion + 5))`
num_kbg=`grep 'weight = 0.00000000' PROCAR |awk NR==1'{print $2}'`
sed -i 's/k-point     /k-point   /g' PROCAR
sed -i 's/k-point    /k-point   /g' PROCAR
# write head
echo "# Kpoint energy" >tmp_head1
for at in $(seq 1 $num_ion)
do
for ob in ion    s     py     pz     px    dxy    dyz    dz2    dxz  x2-y2    tot
do
cp tmp_head1 tmp_hd1
echo "$at$ob" >tmp_head2
paste tmp_hd1 tmp_head2 >tmp_head1
done
done
# take out information of each k point
for i in $(seq $num_kbg $num_kpt)
do
grep -A $num_tkn "k-point   $i" PROCAR >./tmpfd/kbds_$i.dat
echo "i = $i"
done
# taken out information of each k point
# writ fatbands.dat
cd ./tmpfd
for m in $(seq 1 $num_bnd)
do
echo "# band num = $m" >>../tmp_head1
k_path=0
axis_x_o=0
axis_y_o=0
axis_z_o=0
for i in $(seq $num_kbg $num_kpt)
do
axis_x=`grep 'weight = 0.00000000' kbds_$i.dat |awk NR==1'{print $4}'`
axis_y=`grep 'weight = 0.00000000' kbds_$i.dat |awk NR==1'{print $5}'`
axis_z=`grep 'weight = 0.00000000' kbds_$i.dat |awk NR==1'{print $6}'`
awk "BEGIN{print sqrt(($axis_x - $axis_x_o)^2 + ($axis_y-$axis_y_o)^2 + ($axis_z - $axis_z_o)^2)}" >tmppt
dit_k=`cat tmppt`
k_path=`echo "$k_path + $dit_k" | bc -l`
axis_x_o=$axis_x
axis_y_o=$axis_y
axis_z_o=$axis_z
num_en=`expr $(($m - 1)) \* $(($num_ion + 5)) + 3`
energy=`cat kbds_$i.dat |awk NR==$num_en'{print $5}'`
# write a collum
echo "$k_path  $energy  " >tmp_collum1
for io in $(seq 1 $num_ion)
do
num_iotak=`expr 1 \* $(($num_en + 3 + $io))`
cat kbds_$i.dat |awk NR==$num_iotak >tmp_cm
cp tmp_collum1 tmp_col1
paste tmp_col1 tmp_cm >tmp_collum1
done
# end write a collum
cat tmp_collum1 >>../tmp_head1
done
done
cp ../tmp_head1 bandsfat.dat
rm tmp*
cd ..
