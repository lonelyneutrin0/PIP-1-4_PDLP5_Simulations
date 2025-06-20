#!/bin/bash

for i in porinalone porinwithcap
do
	for j in grad nograd
		do
			for k in 0.010 0.150 1.0
				do
				rm ./${i}/${j}/${k}/beta_20/run-*
				rm ./${i}/${j}/${k}/beta_20/run_*
				rm ./${i}/${j}/${k}/beta_20/slurm*
				rm ./${i}/${j}/${k}/beta_20/core* 
			done 

	done
done

