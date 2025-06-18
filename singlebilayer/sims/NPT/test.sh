#!/bin/bash
#SBATCH -C [nvf|nal|nif]
#SBATCH -A vermaaslab
#SBATCH --array=0-0%1
#SBATCH --gres=gpu:1
#SBATCH --gpus-per-task=1
#SBATCH --gres-flags=enforce-binding
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=4:0:0

cd $SLURM_SUBMIT_DIR
#modules are loaded automatically by the NAMD module.
module use /mnt/home/vermaasj/modules
module load NAMD/3.0.1-gpu
NUM=`ls run*dcd | wc -l`
PRINTNUM=`printf "%03d" $NUM`
srun namd3 ++ppn 8 run.namd > run-${PRINTNUM}.log

