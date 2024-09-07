#!/bin/bash
#SBATCH --mem-per-cpu=8GB
#SBATCH --output=test_%A.out 
#SBATCH --ntasks=4
#SBATCH --mail-user=1155194496@link.cuhk.edu.hk
#SBATCH --mail-type=ALL

module load python
source ../../../../ext/py-venv/bin/activate
python cache_stat.py config/SPO2023_stat.yaml
#python output_movgrid2.py
