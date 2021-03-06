#!/bin/tcsh

# documentation: http://www.cesm.ucar.edu/projects/community-projects/LENS/data-sets.html


# variables in array:

set predictand = (prec_t TS)


foreach pred ($predictand)
    # set last parameter to -1 if all states from predictand should be
    # taken, otherwise set length of precursors
    # 5th argument is for bootstrap method.
    sbatch --output=output_$pred.out --error=error_$pred.err --job-name=cl_$pred main_casper_forecast_nn.sh $pred 0 1980 standardized
end

