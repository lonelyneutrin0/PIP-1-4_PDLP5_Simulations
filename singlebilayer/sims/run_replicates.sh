#!/bin/bash

for i in porinalone porinwithcap
do
	cd ./${i}
	for j in grad nograd
		do
			cd ./${j}
			for k in 0.010 0.150 1.0
				do
					cd ./${k}
					for l in 0 1 2
						do
						cd ./${l}
						sbatch -J $i-$j-$k-$l ../../../../submit.sh
						cd ../
						done
					cd ..
				done
			cd ..
		done
	cd ..
done
