# Gold Statistical 0Research
A repository for researching on gold, calculating statistics and testing methods to exploit favorable probabilities in the market. Is it actually possible to find situations with a favorable probability that can be used for profit, or is this not the way to beating the market, through statistical and some technical analysis plus backtesting this will be investigated.   

Several possibilities will be studied and will be listed below.

# Research Questions
1. [Can we identify the minimum percentage move in a 4-hour/1-hour/etc. candle that provides > 75% probability of continued movement for 24+ hours?](##-1.-Minimum-percentage-move-for-a-24h+-continued-movement.)

# Research development
## 1. Minimum percentage move for a 24h+ continued movement.

### 1. Data Collection ([`download_data()`](./xauusd_analyzer.py#L16) / [`load_csv_data()`](./xauusd_analyzer.py#L40))
 * Downloads XAUUSD 4-hour data from Yahoo Finance (Gold Futures: GC=F)
 * Alternative: Load custom CSV data (I mainly used a[ kaggle dataset](https://www.kaggle.com/datasets/novandraanugrah/xauusd-gold-price-historical-data-2004-2024))
 * Timeframe: 2 years of 4-hour candles (~3,107 data points)

### 2. Data Preparation ([`prepare_data()`](./xauusd_analyzer.py#L49)

```ruby
# Calculate percentage changes for each 4H candle
self.data['pct_change'] = ((Close - Open) / Open) * 100

# Classify trading sessions (London/NY/Asian)
# Add volume percentiles for confirmation
# Clean and structure data for analysis
```
