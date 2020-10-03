# Krak

Personal implementation of the Kraken.com [API](https://www.kraken.com/features/api) and [WS](https://docs.kraken.com/websockets/) and a showcase of some of the uses to retrive and analyze the data including the application of a financial algorithm and it's efficency.

## Dependencies
 - pandas
 - requests
 - matplotlib

## Install

```
pip install pipenv
pipenv install
```

## Contents
### KrAPI
  Kraken API implementation library.
### KraWS
  Kraken WS implementation library.
### api_demo
  Showcases how to use krapi
### ws_demo
  Showcases how to use kraws
### mac_plot
  Plots data and shows Moving Average Crossover algorithm application and it's efficency with sharpe ratio (> 1.0 good)
### mac_sratios_eval
  Run the algorithm on various parameters to check which are better (better sharpe ratio)
### ohlc2db
  Fetch ohlc data to a mysql database
### plot_ohlc
  Fetch and plots OHLC data
### publictrades_ohlc_html
  Fetch OHLC and Trades data to prettied html files.
### utility
  Utility methods.

