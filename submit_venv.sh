#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=2G      # increase as needed
#SBATCH --time=0-02:00

module load python/3.6
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index -r requirements.txt
cd $SLURM_TMPDIR && mkdir work && cd work
tar -xf ~/projects/def-najjaran/abtin/Data/DLR/Data.tar.gz
cd Data/Virtual_Simulation/ && mkdir Masks
cd ~/projects/def-najjaran/abtin/Codes/MaskCreator/

python Annotation2MaskConverter.py

cd $SLURM_TMPDIR
tar -cf ~/projects/def-najjaran/abtin/Data/DLR/Results.tar.gz work/Data/Virtual_Simulation/Masks


