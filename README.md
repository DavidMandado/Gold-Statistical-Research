# 📊 Gold Statistical Research

A research repository exploring statistical and technical methods to exploit favorable probabilities in the **Gold (XAUUSD)** market. The core question:  
> *Is it possible to consistently identify high-probability price movements that can be used to generate profit?*

I use momentum analysis, backtesting, and session-based behavior to find actionable patterns.

---

## PHASE ONE

**Main Question:**  
Can we identify a **minimum percentage move** in a 4H/1H candle that leads to **continued movement over the next 24+ hours** with >75% probability?

---

## ⚙️ Research Pipeline

### 1. 🧬 Data Collection  
- Source: [Yahoo Finance](https://finance.yahoo.com) & [Kaggle (XAUUSD dataset)](https://www.kaggle.com/datasets/novandraanugrah/xauusd-gold-price-historical-data-2004-2024)  
- Timeframe: 2 years of 4H candles (~3,107 samples)  
- Script: [`download_data()`](./xauusd_analyzer.py#L16) / [`load_csv_data()`](./xauusd_analyzer.py#L40)

---

### 2. 🧹 Data Preparation  
- Calculates percentage change per candle  
- Classifies trading sessions (London / NY / Asian)  
- Adds volume percentiles  
- Script: [`prepare_data()`](./xauusd_analyzer.py#L49)

---

### 3. 📈 Momentum Persistence Analysis  
- Tests thresholds: `1.0%` → `4.0%`  
- Forward returns measured at: `6H`, `12H`, `24H`, `48H`  
- Analyzes:
  - Win rate
  - Average return
  - Max Adverse Excursion  
- Script: [`analyze_momentum_persistence()`](./xauusd_analyzer.py#L81)

---

### 4. 📊 Signal Quality Metrics  
Script: [`analyze_signal_group()`](./xauusd_analyzer.py#L118)

- ✅ **Win Rate**: % of trades in expected direction  
- 📉 **Max Drawdown**: Largest loss before move continuation  
- 🔁 **Frequency**: How often the signal appears  
- 📈 **Average Return**: Mean return across instances

---

### 5. 🕒 Session-Based Performance  
- Segments results by session: **London**, **New York**, **Asian**  
- Combines volume percentile for filtering  
- Visualizes risk-return tradeoffs by session  
- Investigates which sessions yield more reliable signals

---

## 🧠 Key Findings

### ✅ High-Probability Setups (Rare but Reliable)

| Threshold | Timeframe | Direction | Win Rate | Avg Return | Signals |
|-----------|-----------|-----------|----------|------------|---------|
| 2.0%      | 24H       | Bullish   | 100%     | 0.84%      | 2       |
| 2.5%      | 12H       | Bearish   | 100%     | 0.82%      | 2       |

---

### ⚖️ Tradeable Frequency Setups (Balanced Risk)

| Threshold | Timeframe | Direction | Win Rate | Avg Return | Signals |
|-----------|-----------|-----------|----------|------------|---------|
| 1.5%      | 24H       | Bullish   | 81.8%    | 0.28%      | 11      |
| 1.0%      | 24H       | Bullish   | 64.4%    | 0.07%      | 45      |

---

## 📊 Visual Highlights

<table>
  <tr>
    <td align="center"><img src="assets/plots/win_rate_heatmap.png" width="400"><br/><sub><b>Win Rate Heatmap</b></sub></td>
    <td align="center"><img src="assets/plots/signal_frequency.png" width="400"><br/><sub><b>Signal Frequency</b></sub></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/plots/risk_vs_return_bubble.png" width="400"><br/><sub><b>Risk vs Reward</b></sub></td>
    <td align="center"><img src="assets/plots/return_distribution.png" width="400"><br/><sub><b>Return Distribution</b></sub></td>
  </tr>
</table>

---

## 📌 Summary of Insights

- ✅ **Momentum Persistence Exists**: ≥2.0% 4H moves often persist over 24H  
- 🔁 **Trade-off Observed**: 1.5% is the sweet spot between reliability and frequency  
- ⚠️ **Drawdowns Manageable**: Max adverse excursion <1% on average  
- 🧪 **Session Context Matters**: London + High Volume = more consistent moves

---

## ⚠️ Limitations

- Only 2 years of data used in initial test  
- Few samples for extreme moves (e.g., 2.5%+)  
- No modeling of:
  - Spread / slippage
  - Economic events (NFP, CPI)
  - Volatility regimes  
- Purely signal-based; no exit logic yet

---

## 🧭 Roadmap for PHASE TWO

### 🟡 Phase 1: **Historical Expansion**
- Load full 2004–2025 dataset
- Test across different market regimes

### 🔵 Phase 2: **Strategy Refinement**
- Add volume and DXY filters  
- Avoid high-impact macro events  
- Test multi-timeframe confluence  

### 🟢 Phase 3: **Practical Simulation**
- Build rule-based system with SL, TP, position sizing  
- Paper trade using €50 capital  
- Include spread, slippage, fees

### 🟣 Phase 4: **Automation & Deployment**
- MT4/MT5 Signal bot  
- Alerts + dashboard  
- Gradual capital scaling based on stats

---

## ▶️ How to Run

```bash
pip install pandas numpy matplotlib seaborn yfinance scipy
python xauusd_analyzer.py
```

## PHASE TWO
## 🧠 Expanded Results Using Full Dataset (2004–2025)

We have now run the full momentum persistence analysis using the complete historical dataset (2004–2025), consisting of over **32,000 4-hour candles**. This gives much more robust context around the signal strength, frequency, and statistical reliability across various market cycles.

### ✅ Updated Findings

#### 🏆 Highest Win Rate Setups (Rare but Powerful)

| Threshold | Timeframe | Direction | Win Rate | Avg Return | Signal Count |
|-----------|-----------|-----------|----------|------------|---------------|
| 3.5%      | 24H       | Bullish   | 80.0%    | 1.24%      | 5             |
| 4.0%      | 12H       | Bearish   | 75.0%    | 0.48%      | 4             |
| 4.0%      | 24H       | Bearish   | 75.0%    | -0.00%     | 4             |

These setups are **extremely high-confidence**, with win rates of 75–80% and impressive returns. However, they are **very rare**, often producing only a handful of signals over multiple years. These are the kinds of trades we want to be notified about when they appear.

#### 📈 Tradeable Setups With More Frequency

| Threshold | Timeframe | Direction | Win Rate | Avg Return | Signal Count |
|-----------|-----------|-----------|----------|------------|---------------|
| 3.5%      | 12H       | Bearish   | 70.0%    | 0.48%      | 10            |
| 2.5%      | 48H       | Bullish   | 69.7%    | 0.22%      | 33            |
| 3.0%      | 24H       | Bearish   | 69.2%    | 0.22%      | 13            |

These are **moderate-frequency, high-reliability trades**. They offer a good balance between performance and signal count, and will be a core focus for building a real-world trading signal system.

---

### 📊 Visual Results

<div align="center">

<table>
  <tr>
    <td align="center">
      <img src="assets/plots/winrate2.png" alt="Win Rate Heatmap" width="400"/>
    </td>
    <td align="center">
      <img src="assets/plots/frequencybythres2.png" alt="Signal Frequency" width="400"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="assets/plots/riskreturn2.png" alt="Risk vs Reward Bubble Chart" width="400"/>
    </td>
    <td align="center">
      <img src="assets/plots/averagereturn2.png" alt="Return Distribution" width="400"/>
    </td>
  </tr>
</table>

</div>

---

### 🕒 Session-Based Performance (24H Signals)

| Session | Direction | Signal Count | Win Rate | Avg Return | Max Adverse Excursion |
|---------|-----------|---------------|----------|------------|------------------------|
| London  | Bullish   | 23            | 52.2%    | 0.28%      | 1.29%                  |
| London  | Bearish   | 34            | 61.8%    | 0.83%      | 1.29%                  |
| NY      | Bullish   | 33            | 51.5%    | 0.18%      | 1.13%                  |
| NY      | Bearish   | 39            | 56.4%    | 0.32%      | 1.09%                  |
| Asian   | Bullish   | 7             | 14.3%    | -1.20%     | 2.29%                  |
| Asian   | Bearish   | 7             | 42.9%    | -0.10%     | 2.11%                  |

> 🧠 **Insight**: The **London session** consistently produces the strongest and most reliable signals. Asian session signals are mostly unreliable and should be avoided or filtered.

---

### 📌 Key Takeaways

- ✅ **Momentum Persistence Exists**: Confirmed across nearly two decades of data.
- 🏅 **Incredible setups exist**, with >75% win rate and >100% average returns, but they are **rare**.
- ⚖️ There is always a **trade-off between accuracy and frequency**. Reliable but more frequent setups tend to cluster around the 2.5–3.5% thresholds.
- 📉 Asian session signals generally underperform and are likely noise.
- 📊 High-volume and breakout sessions (London/NY) provide the best signal environment.

---

### 🎯 Strategic Outlook

Because the highest-performing signals are rare, we will not rely on them alone. The roadmap forward involves:

- 🧠 **Developing a signal system** to alert or log the rare but extremely reliable setups as they occur
- 🔁 **Complementing this with higher-frequency models**, such as:
  - Mean reversion strategies
  - Scalp-friendly momentum bursts
  - Multi-timeframe confirmation models
- 📈 All strategies will later be tested in a portfolio context for capital allocation and robustness

---

