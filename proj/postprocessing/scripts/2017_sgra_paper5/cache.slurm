#!/bin/bash
#SBATCH --mem-per-cpu=4GB
#SBATCH --output=test_%A.out 
#SBATCH --ntasks=4
#SBATCH --mail-user=1155194496@link.cuhk.edu.hk
#SBATCH --mail-type=ALL

module load python
source ../../../../ext/py-venv/bin/activate
python cache_gt.py config/SPO2023_gt.yaml
#python output_movgrid2.py
