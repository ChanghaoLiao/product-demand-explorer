# Product Demand Explorer

An interactive Streamlit dashboard for internal operations managers and demand planners. It explores net demand and underlying order-record activity for two anonymized products across 2014–2016.

## Features

- Product, date-range, and time-granularity filters
- Dynamic plain-language key insights
- Demand trend and period comparison charts
- Order-record activity heatmap
- Filtered daily data table

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Data source and license

The included daily file is a transformed subset of FelixZhao's [Forecasts for Product Demand](https://www.kaggle.com/datasets/felixzhao/productdemandforecasting) dataset. The source dataset is published under the GNU General Public License v2.0. Product identifiers are anonymized, and this app does not interpret demand as confirmed sales.

The transformed data is redistributed under GPL-2.0-only. See `LICENSE`.

