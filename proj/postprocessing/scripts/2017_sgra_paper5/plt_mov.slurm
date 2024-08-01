#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=16gb
#SBATCH --mail-user=1155194496@link.cuhk.edu.hk
#SBATCH --mail-type=END
#SBATCH --array=0-2

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load python
source ../../../../ext/py-venv/bin/activate

python output_movgrid2.py ${SLURM_ARRAY_TASK_ID}
