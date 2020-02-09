# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:19:19 2017

@author: sonja
"""
# import libraries
import numpy as np
from classes.Precursors import Precursors
from classes.Predictand import Predictand
from classes.Forecast import Forecast
from classes.ExportVarPlot import ExportVarPlot
import sys
from scipy import stats


# usage TS ini/composites_America_ICEFRAC.ini ICEFRAC prec_t 6009 99

def main():
    logger.info("Start forecast model")

    # load inifile according to variable
    var = sys.argv[1]
    inifile = f"ini/clusters_America_{var}.ini"
    predictand = Predictand(inifile)

    # load forecast-parameters
    method_name = 'ward'
    k = 6
    forecast = Forecast(inifile, k, method_name)
    logger.info("Clusters: " + str(forecast.k))
    diff = int(forecast.end_year) - int(forecast.beg_year)
    forecast_data = np.zeros((diff, predictand.dict_pred_1D[f"{predictand.var}"].shape[1]))
    pattern_corr_values = []

    # load precursors
    precursors = Precursors(inifile)
    all_precs_names = [x for x in precursors.dict_precursors.keys()]

    # Calculate forecast for all years
    for year in range(int(forecast.beg_year), int(forecast.beg_year) + 3):  # int(forecast.end_year)

        # Calculate clusters of precursors for var, by removing one year
        predictand.calculate_clusters(forecast.method_name, forecast.k, year - forecast.beg_year)

        # Calculate composites
        precursors.get_composites_data_1d(year - forecast.beg_year, predictand.f, forecast.k, forecast.method_name,
                                          predictand.var)

        # Prediction
        forecast_temp = forecast.prediction(predictand.clusters, precursors.dict_composites,
                                            precursors.dict_prec_1D, year - forecast.beg_year)

        # Assign forecast data to array
        forecast_data[year - forecast.beg_year] = forecast_temp

        # Calculate pattern correlation
        pattern_corr_values.append(stats.pearsonr(forecast_data[year - forecast.beg_year],
                                                  predictand.dict_standardized_pred_1D[f"{predictand.var}"][
                                                      year - forecast.beg_year])[0])

    # Calculate time correlation for each point
    time_correlation, significance = forecast.calculate_time_correlation(
        predictand.dict_standardized_pred_1D[f"{predictand.var}"],
        forecast_data, predictand.time_start_file)

    # Reshape correlation maps
    pred_t_corr_reshape = np.reshape(time_correlation, (predictand.dict_predict[predictand.var].shape[1],
                                                                      predictand.dict_predict[predictand.var].shape[2]))
    significance_corr_reshape = np.reshape(significance, (predictand.dict_predict[predictand.var].shape[1],
                                                          predictand.dict_predict[predictand.var].shape[2]))

    logger.info(f'time correlation: {np.nanmean(pred_t_corr_reshape)}')
    logger.info(f'pattern correlation: {np.nanmean(pattern_corr_values)}')

    # Plot correlation map, if specified in ini-file
    if forecast.plot:
        logger.info("Plot and save variables")
        ex = ExportVarPlot()
        ex.save_plot_and_time_correlation(forecast.list_precursors, predictand, pred_t_corr_reshape,
                                          significance_corr_reshape, all_precs_names)


if __name__ == '__main__':
    import logging.config
    from config_dict import config

    logger = logging.getLogger(__name__)
    logging.config.dictConfig(config)
    logger.info("Start clustering program")
    main()
