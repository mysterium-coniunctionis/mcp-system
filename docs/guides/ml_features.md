# Machine Learning Features

## Available Models

### Time Series Analysis
- Prophet forecasting
- ARIMA modeling
- Seasonal decomposition

### Anomaly Detection
- Isolation Forest
- DBSCAN clustering
- Autoencoder methods

### Pattern Recognition
- PCA dimensionality reduction
- K-means clustering
- Feature importance analysis

## Implementation Examples
```python
# Time series forecasting
from mcp_demo.analysis.ml import TimeSeriesForecaster

forecaster = TimeSeriesForecaster()
forecasts = forecaster.predict(metrics, horizon='24h')
```