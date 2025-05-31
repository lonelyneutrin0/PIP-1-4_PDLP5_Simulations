#!/bin/bash

for i in porinalone
do
	for j in grad nograd
		do
			for k in 0.010 0.150 
				do
				rm ./${i}./${j}./${k}/0/run-*
				rm ./${i}./${j}./${k}/0/run_*
				rm ./${i}./${j}./${k}/0/slurm*
			done

	done
done

