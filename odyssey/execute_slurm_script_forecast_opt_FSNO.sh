#!/bin/bash

# documentation: http://www.cesm.ucar.edu/projects/community-projects/LENS/data-sets.html
# set last parameter to -1 if all states from predictand should be
# taken, otherwise set length of precursors
# 5th argument is for bootstrap method.

# variables in array:
# predictand=( prec_t TS )
predictand=( TS )
# precursors=(FSNO-America FSNO-Eurasia  ICEFRAC Z500 SST PSL)

precursors=(FSNO-America FSNO-Eurasia)
#precursors=(SST)

for pred in "${predictand[@]}"
do
    for var in "${precursors[@]}"
    do
        sbatch --output=output_opt_${pred}_${var}.out --error=error_opt_${pred}_${var}.err --job-name=cl_opt_$pred main_odyssey_forecast_opt_FSNO.sh ${pred} ${var} 0 1980 standardized-opt
    done
done
