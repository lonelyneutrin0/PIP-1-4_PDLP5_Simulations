#!/bin/bash

for i in porinalone porinwithcap
do
	cd ./${i}
	for j in grad nograd
		do
			cd ./${j}
			for k in 0.010 0.150 1.0
				do
					cd ./${k}/0
					sbatch -J $i-$j-$k ../../../../submit.sh
					cd ../../
				done
			cd ..
		done
	cd ..
done
