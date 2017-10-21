#!/bin/bash
#SBATCH -J ToricCodeLong
#SBATCH --partition  smp
#SBATCH -N 4
#SBATCH -n 10 
#SBATCH --mem=40G
#SBATCH --time=40:00:00

#SBATCH -o longout.out
#SBATCH -e longerr.err

#module load gnutools/2.69

/bin/date
python CodePy2/varmain.py
/bin/date

exit 0

# eof
