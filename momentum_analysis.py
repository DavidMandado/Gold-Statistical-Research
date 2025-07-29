from xauusd_analyzer import XAUUSDMomentumAnalyzer

# Initialize
analyzer = XAUUSDMomentumAnalyzer()

# Download 2 years of 4H data
analyzer.download_data(period="2y", interval="4h")

# Run analysis
results = analyzer.analyze_momentum_persistence()

# Find your 80% win rate combinations
optimal = analyzer.find_optimal_thresholds(min_win_rate=80, min_signals=20)