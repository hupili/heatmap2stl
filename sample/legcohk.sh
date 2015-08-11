#!/bin/bash

#heatmap2py <fn_data> <start_x> <end_x> <start_y> <end_y> <substrate_height> <gap_width> <scale_x> <scale_y> <scale_z>

exe="python ../heatmap2stl.py"
sh=0.1
gw=0.2
sx=4
sy=4
sz=20

rm -rf stl
mkdir -p stl

$exe mv-relation.json 00 25 00 25 $sh $gw $sx $sy $sz > stl/block-0-0.stl
$exe mv-relation.json 25 50 00 25 $sh $gw $sx $sy $sz > stl/block-0-1.stl
$exe mv-relation.json 50 70 00 25 $sh $gw $sx $sy $sz > stl/block-0-2.stl

$exe mv-relation.json 00 25 25 50 $sh $gw $sx $sy $sz > stl/block-1-0.stl
$exe mv-relation.json 25 50 25 50 $sh $gw $sx $sy $sz > stl/block-1-1.stl
$exe mv-relation.json 50 70 25 50 $sh $gw $sx $sy $sz > stl/block-1-2.stl

$exe mv-relation.json 00 25 50 70 $sh $gw $sx $sy $sz > stl/block-2-0.stl
$exe mv-relation.json 25 50 50 70 $sh $gw $sx $sy $sz > stl/block-2-1.stl
$exe mv-relation.json 50 70 50 70 $sh $gw $sx $sy $sz > stl/block-2-2.stl

#python heatmap2stl.py mv-relation.json 00 22 00 22 0.1 0.2 5 5 10 > stl/block-0-0.stl
#python heatmap2stl.py mv-relation.json 25 50 00 25 0.1 0.2 5 5 10 > stl/block-0-1.stl
#python heatmap2stl.py mv-relation.json 50 70 00 25 0.1 0.2 5 5 10 > stl/block-0-2.stl
#
#python heatmap2stl.py mv-relation.json 00 25 25 50 0.1 0.2 5 5 10 > stl/block-1-0.stl
#python heatmap2stl.py mv-relation.json 25 50 25 50 0.1 0.2 5 5 10 > stl/block-1-1.stl
#python heatmap2stl.py mv-relation.json 50 70 25 50 0.1 0.2 5 5 10 > stl/block-1-2.stl
#
#python heatmap2stl.py mv-relation.json 00 25 50 70 0.1 0.2 5 5 10 > stl/block-2-0.stl
#python heatmap2stl.py mv-relation.json 25 50 50 70 0.1 0.2 5 5 10 > stl/block-2-1.stl
#python heatmap2stl.py mv-relation.json 50 70 50 70 0.1 0.2 5 5 10 > stl/block-2-2.stl
#
