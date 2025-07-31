# Gold Statistical Research
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

  ### 3. Momentum Persistence Analysis ([`analyze_momentum_persistence()`](./xauusd_analyzer.py#L81))
  * Tests multiple threshold levels: 1.0%, 1.5%, 2.0%, 2.5%, 3.0%, 3.5%, 4.0%, to see which one can give us the quickest entry into a intraday movement.
  * Analyzes lookforward periods: 6H, 12H, 24H, 48H
  * Calculates win rates, average returns, and risk metrics
  * Separates bullish and bearish signals

  ### 4. Signal Analysis (['analyze_signal_group()'](./xauusd_analyzer.py#L118))

  * Win Rate: Percentage of trades that moved in expected direction
  * Average Return: Mean percentage move over the timeframe
  * Maximum Adverse Excursion: Worst drawdown before reaching target
  * Signal Frequency: How often these setups occur

  ### 5. Trading Session & Contextual Analysis

  * Compares momentum signal performance across London, New York, and Asian trading sessions
  * Analyzes volume confirmation using percentile ranks
  * Highlights which sessions produce more reliable continuation signals
  * Includes risk-reward visualizations by session

  ### 6. Key Findings

  #### High-Probability Setups (Rare but Reliable)
  | Threshold | Timeframe | Direction | Win Rate | Avg Return | Signal Count |
  |-----------|-----------|-----------|----------|------------|---------------|
  | 2.0%      | 24H       | Bullish   | 100%     | 0.84%      | 2             |
  | 2.0%      | 12H       | Bullish   | 100%     | 0.64%      | 2             |
  | 2.5%      | 12H       | Bearish   | 100%     | 0.82%      | 2             |

  #### Tradeable Frequency Setups (Moderate Risk-Reward)
  | Threshold | Timeframe | Direction | Win Rate | Avg Return | Signal Count |
  |-----------|-----------|-----------|----------|------------|---------------|
  | 1.5%      | 24H       | Bullish   | 81.8%    | 0.28%      | 11            |
  | 1.0%      | 24H       | Bullish   | 64.4%    | 0.07%      | 45            |

  ### 7. Visual Insights

  <div align="center">

  <table>
    <tr>
      <td align="center">
        <img src="assets/plots/win_rate_heatmap.png" alt="Win Rate Heatmap" width="400"/>
      </td>
      <td align="center">
        <img src="assets/plots/signal_frequency.png" alt="Signal Frequency" width="400"/>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="assets/plots/risk_vs_return_bubble.png" alt="Risk vs Reward Bubble Chart" width="400"/>
      </td>
      <td align="center">
        <img src="assets/plots/return_distribution.png" alt="Return Distribution" width="400"/>
      </td>
    </tr>
  </table>

  </div>


  * **Win Rate Heatmap**: Highlights 80%+ win-rate zones around 2.0% thresholds
  * **Signal Frequency Chart**: Shows inverse relationship between frequency and accuracy
  * **Risk vs Return Bubbles**: Visualizes optimal zones for threshold selection
  * **Average Return Distribution**: Confirms best risk-adjusted returns at 2.0% over 24H

  ### 8. Statistical Conclusions

  * **Momentum Persistence Exists**: ≥2.0% moves often persist over 24 hours
  * **Accuracy vs Frequency Trade-off**: 1.5% is a sweet spot between signal reliability and frequency
  * **Risk Metrics**: Max adverse excursion generally <1%; 24H holds outperform shorter durations

  ### 9. Limitations

  * Limited to 2 years of data; higher thresholds have few samples
  * Does not include macroeconomic event filters or volatility regime awareness
  * No execution slippage, spread, or fee simulation in initial backtest

  ### 10. Next Steps

  #### Phase 1: Enhanced Data Analysis
  * Use full Kaggle dataset (2004–2025)
  * Test momentum persistence across economic cycles

  #### Phase 2: Strategy Refinement
  * Add volume filters, multi-timeframe confluence, DXY correlation
  * Integrate economic calendar to avoid high-impact news events

  #### Phase 3: Practical Implementation
  * Validate with paper trading for 1–2 months
  * Add stop-loss, position sizing logic for €50 capital
  * Test realistic performance including slippage and fees

  #### Phase 4: Live Trading Prep
  * MT4/MT5 signal integration
  * Alert system + dashboard
  * Gradual capital scaling based on results

  ### 11. How to Run

  ```ruby
  pip install pandas numpy matplotlib seaborn yfinance scipy
  python xauusd_analyzer.py
  ```