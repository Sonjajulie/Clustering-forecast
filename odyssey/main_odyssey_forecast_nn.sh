#!/bin/bash
#SBATCH -J clusters_$pred
#SBATCH -p shared # Partition
#SBATCH -n 1
#SBATCH -t 2-00:00          # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH --mem=8G  # Memory request (8Gb)
#SBATCH --ntasks-per-node=8
#SBATCH -o output_$pred.out
#SBATCH -e error_$pred.err


pred=$1
precursor=$2
datamin=$3
datamax=$4
outputlabel=$5
echo $pred
echo $precursor

module load python
source activate clustering-forecast

python3 ../main_cluster_forecast_all_precursors_nn.py -ini ../ini/clusters_America_${pred}_Forecast_ncar.ini --outputlabel $outputlabel --predictand $pred --forecast_precursors ${precursor} --logfile logs/log_${pred}_${precursor}.log --datarange $datamin $datamax

