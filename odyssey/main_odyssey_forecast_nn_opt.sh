#!/bin/bash
#SBATCH -J clusters_$pred
#SBATCH -p shared # Partition
#SBATCH -n 1
#SBATCH -t 1-00:00          # Runtime in D-HH:MM, minimum of 10 minutes
#SBATCH --mem=6G  # Memory request (8Gb)
#SBATCH --ntasks-per-node=6
#SBATCH -o output_$pred.out
#SBATCH -e error_$pred.err


pred=$1
datamin=$2
datamax=$3
outputlabel=$4
echo $pred

module load python
source activate clustering-forecast

python3 ../main_cluster_forecast_all_precursors_nn_opt.py -ini ../ini/clusters_America_${pred}_Forecast_opt.ini --outputlabel $outputlabel --predictand $pred --logfile logs/log_${pred}.log --datarange $datamin $datamax

