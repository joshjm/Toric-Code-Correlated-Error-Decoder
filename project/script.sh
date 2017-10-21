#!/bin/bash
#SBATCH -J ToricCodeLong
#SBATCH --partition  smp
	
#SBATCH -n 100 
#SBATCH --mem=150G
#SBATCH --time=40:00:00

#SBATCH -o out.out
#SBATCH -e err.err

#module load gnutools/2.69

/bin/date
python CodePy2/varmain.py
/bin/date

exit 0

# eof
