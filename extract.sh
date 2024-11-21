#!/bin/bash
#BSUB -J extract           
#BSUB -o extract.out    
#BSUB -e extract.err    
#BSUB -n 1               
#BSUB -q normal

while read -r line;do
   less sentence1.txt  | grep "$line" >>sentresult.txt
done<genelist.txt1
