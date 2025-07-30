import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class XAUUSDMomentumAnalyzer:
    def __init__(self):
        self.data = None
        self.results = {}
        
    def download_data(self, period="2y", interval="4h"):
        """
        Download XAUUSD data from Yahoo Finance
        period: "1y", "2y", "5y", "max"
        interval: "1h", "4h", "1d"
        """
        print("Downloading XAUUSD data...")
        
        # Download gold futures data (GC=F is gold futures)
        ticker = "GC=F"  # Gold futures
        self.data = yf.download(ticker, period=period, interval=interval)
        
        if self.data.empty:
            print("Failed to download data. Trying alternative ticker...")
            # Try XAU=X (spot gold)
            ticker = "XAU=X"
            self.data = yf.download(ticker, period=period, interval=interval)
        
        if not self.data.empty:
            print(f"Downloaded {len(self.data)} candles of {ticker}")
            self.prepare_data()
        else:
            print("Failed to download data. You'll need to load your own CSV file.")
            
    def load_csv_data(self, filepath):
        """
        Load data from CSV file
        Expected columns: DateTime, Open, High, Low, Close, Volume
        """
        self.data = pd.read_csv(filepath, parse_dates=['DateTime'], index_col='DateTime')
        print(f"Loaded {len(self.data)} candles from CSV")
        self.prepare_data()
        
    def prepare_data(self):
        """Prepare data for analysis"""
        # Calculate percentage changes
        self.data['pct_change'] = ((self.data['Close'] - self.data['Open']) / self.data['Open']) * 100
        
        # Add session information
        self.data['hour'] = self.data.index.hour
        self.data['session'] = self.data['hour'].apply(self.get_trading_session)
        
        # Add day of week
        self.data['day_of_week'] = self.data.index.dayofweek
        
        # Calculate volume percentile (if volume data exists)
        if 'Volume' in self.data.columns:
            self.data['volume_percentile'] = self.data['Volume'].rolling(100).rank(pct=True)
        else:
            self.data['volume_percentile'] = 0.5  # Default to median
            
        # Remove NaN values
        self.data = self.data.dropna()
        
    def get_trading_session(self, hour):
        """Classify trading sessions based on hour (UTC)"""
        if 8 <= hour < 16:
            return 'London'
        elif 13 <= hour < 21:
            return 'NY'
        elif 21 <= hour or hour < 8:
            return 'Asian'
        else:
            return 'Overlap'
            
    def analyze_momentum_persistence(self, thresholds=None, lookforward_hours=None):
        """
        Main analysis: test momentum persistence at different thresholds
        """
        if thresholds is None:
            thresholds = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
            
        if lookforward_hours is None:
            lookforward_hours = [6, 12, 24, 48]  # Hours to look forward
            
        results = []
        
        print("Analyzing momentum persistence...")
        
        for threshold in thresholds:
            for hours in lookforward_hours:
                # Find signals (candles that moved more than threshold)
                bullish_signals = self.data[self.data['pct_change'] >= threshold].copy()
                bearish_signals = self.data[self.data['pct_change'] <= -threshold].copy()
                
                # Analyze bullish signals
                bull_stats = self.analyze_signal_group(bullish_signals, hours, 'bullish')
                bull_stats['threshold'] = threshold
                bull_stats['hours'] = hours
                bull_stats['direction'] = 'bullish'
                results.append(bull_stats)
                
                # Analyze bearish signals
                bear_stats = self.analyze_signal_group(bearish_signals, hours, 'bearish')
                bear_stats['threshold'] = threshold
                bear_stats['hours'] = hours
                bear_stats['direction'] = 'bearish'
                results.append(bear_stats)
                
        self.results = pd.DataFrame(results)
        return self.results
        
    def analyze_signal_group(self, signals, hours, direction):
        """Analyze a group of signals (bullish or bearish)"""
        if len(signals) == 0:
            return {
                'signal_count': 0,
                'win_rate': 0,
                'avg_return': 0,
                'avg_winner': 0,
                'avg_loser': 0,
                'max_adverse': 0,
                'avg_time_to_target': 0
            }
            
        periods_ahead = hours // 4  # Convert hours to 4H periods
        
        wins = 0
        returns = []
        winners = []
        losers = []
        max_adverse_moves = []
        
        for idx in signals.index:
            try:
                # Get the position of current candle
                current_pos = self.data.index.get_loc(idx)
                
                # Check if we have enough future data
                if current_pos + periods_ahead >= len(self.data):
                    continue
                    
                # Get current and future prices
                current_close = float(self.data.iloc[current_pos]['Close'])
                
                # Get future price range
                future_data = self.data.iloc[current_pos + 1:current_pos + periods_ahead + 1]
                if len(future_data) == 0:
                    continue
                    
                future_close = float(future_data['Close'].iloc[-1])
                
                # Calculate the move over the lookforward period
                total_return = ((future_close - current_close) / current_close) * 100
                
                # Calculate maximum adverse excursion
                if direction == 'bullish':
                    max_adverse = ((float(future_data['Close'].min()) - current_close) / current_close) * 100
                    success = bool(total_return > 0)
                else:
                    max_adverse = ((float(future_data['Close'].max()) - current_close) / current_close) * 100
                    success = bool(total_return < 0)
                    total_return = -total_return  # Make positive for easier analysis
                
                returns.append(total_return)
                max_adverse_moves.append(abs(max_adverse))
                
                if success:
                    wins += 1
                    winners.append(total_return)
                else:
                    losers.append(total_return)
                    
            except (IndexError, KeyError):
                continue
                
        total_signals = len(returns)
        
        return {
            'signal_count': total_signals,
            'win_rate': (wins / total_signals * 100) if total_signals > 0 else 0,
            'avg_return': np.mean(returns) if returns else 0,
            'avg_winner': np.mean(winners) if winners else 0,
            'avg_loser': np.mean(losers) if losers else 0,
            'max_adverse': np.mean(max_adverse_moves) if max_adverse_moves else 0,
            'avg_time_to_target': hours  # Simplified for now
        }
        
    def find_optimal_thresholds(self, min_win_rate=80, min_signals=20):
        """Find thresholds that meet minimum criteria"""
        if self.results is None or len(self.results) == 0:
            print("No results available. Run analyze_momentum_persistence() first.")
            return None
            
        # Filter results by criteria
        optimal = self.results[
            (self.results['win_rate'] >= min_win_rate) &
            (self.results['signal_count'] >= min_signals) &
            (self.results['avg_return'] > 0)
        ].copy()
        
        if len(optimal) == 0:
            print(f"No combinations meet criteria (win_rate >= {min_win_rate}%, signals >= {min_signals})")
            # Show best alternatives
            best_by_winrate = self.results.nlargest(10, 'win_rate')
            print("\nBest win rates found:")
            print(best_by_winrate[['threshold', 'hours', 'direction', 'win_rate', 'signal_count', 'avg_return']].round(2))
            return best_by_winrate
        
        # Rank by win rate and average return
        optimal['score'] = optimal['win_rate'] * optimal['avg_return'] / 100
        optimal = optimal.sort_values('score', ascending=False)
        
        print(f"Found {len(optimal)} combinations meeting criteria:")
        print(optimal[['threshold', 'hours', 'direction', 'win_rate', 'signal_count', 'avg_return', 'score']].round(2))
        
        return optimal
        
    def analyze_by_session(self, threshold=2.0, hours=24):
        """Analyze performance by trading session"""
        session_results = []
        
        for session in ['London', 'NY', 'Asian', 'Overlap']:
            session_data = self.data[self.data['session'] == session]
            
            bullish_signals = session_data[session_data['pct_change'] >= threshold]
            bearish_signals = session_data[session_data['pct_change'] <= -threshold]
            
            bull_stats = self.analyze_signal_group(bullish_signals, hours, 'bullish')
            bear_stats = self.analyze_signal_group(bearish_signals, hours, 'bearish')
            
            session_results.append({
                'session': session,
                'direction': 'bullish',
                **bull_stats
            })
            
            session_results.append({
                'session': session,
                'direction': 'bearish',
                **bear_stats
            })
            
        return pd.DataFrame(session_results)
        
    def plot_results(self):
        """Create visualizations of the results"""
        if self.results is None or len(self.results) == 0:
            print("No results to plot. Run analysis first.")
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Win Rate by Threshold
        pivot_winrate = self.results.pivot_table(
            values='win_rate', 
            index='threshold', 
            columns=['hours', 'direction'], 
            aggfunc='mean'
        )
        
        sns.heatmap(pivot_winrate, annot=True, fmt='.1f', cmap='RdYlGn', 
                   ax=axes[0,0], cbar_kws={'label': 'Win Rate (%)'})
        axes[0,0].set_title('Win Rate by Threshold and Timeframe')
        
        # Plot 2: Signal Count by Threshold
        pivot_signals = self.results.pivot_table(
            values='signal_count', 
            index='threshold', 
            columns=['hours', 'direction'], 
            aggfunc='mean'
        )
        
        sns.heatmap(pivot_signals, annot=True, fmt='.0f', cmap='Blues', 
                   ax=axes[0,1], cbar_kws={'label': 'Signal Count'})
        axes[0,1].set_title('Signal Frequency by Threshold and Timeframe')
        
        # Plot 3: Average Return by Threshold
        pivot_return = self.results.pivot_table(
            values='avg_return', 
            index='threshold', 
            columns=['hours', 'direction'], 
            aggfunc='mean'
        )
        
        sns.heatmap(pivot_return, annot=True, fmt='.2f', cmap='RdYlBu', 
                   ax=axes[1,0], cbar_kws={'label': 'Avg Return (%)'})
        axes[1,0].set_title('Average Return by Threshold and Timeframe')
        
        # Plot 4: Risk-Reward Scatter
        valid_results = self.results[self.results['signal_count'] > 10]
        scatter = axes[1,1].scatter(valid_results['max_adverse'], valid_results['avg_return'], 
                                  c=valid_results['win_rate'], s=valid_results['signal_count']*2,
                                  cmap='RdYlGn', alpha=0.7)
        axes[1,1].set_xlabel('Max Adverse Move (%)')
        axes[1,1].set_ylabel('Average Return (%)')
        axes[1,1].set_title('Risk vs Return (color=win_rate, size=signal_count)')
        plt.colorbar(scatter, ax=axes[1,1], label='Win Rate (%)')
        
        plt.tight_layout()
        plt.show()
        
    def summary_report(self):
        """Generate a summary report of findings"""
        if self.results is None:
            print("No analysis completed yet.")
            return
            
        print("=== XAUUSD MOMENTUM PERSISTENCE ANALYSIS REPORT ===\n")
        
        # Data overview
        print(f"Analysis Period: {self.data.index[0]} to {self.data.index[-1]}")
        print(f"Total Candles Analyzed: {len(self.data)}")
        print(f"Average 4H Move: {self.data['pct_change'].mean():.3f}%")
        print(f"Move Standard Deviation: {self.data['pct_change'].std():.3f}%\n")
        
        # Best performing combinations
        print("TOP 5 COMBINATIONS BY WIN RATE:")
        top_by_winrate = self.results.nlargest(5, 'win_rate')
        for _, row in top_by_winrate.iterrows():
            print(f"{row['threshold']}% threshold, {row['hours']}H lookforward, {row['direction']}: "
                  f"{row['win_rate']:.1f}% win rate, {row['signal_count']} signals, "
                  f"{row['avg_return']:.2f}% avg return")
        
        print("\nCOMBINATIONS WITH 70%+ WIN RATE AND 20+ SIGNALS:")
        good_combos = self.results[
            (self.results['win_rate'] >= 70) & 
            (self.results['signal_count'] >= 20)
        ].sort_values('win_rate', ascending=False)
        
        if len(good_combos) > 0:
            for _, row in good_combos.iterrows():
                print(f"{row['threshold']}% threshold, {row['hours']}H lookforward, {row['direction']}: "
                      f"{row['win_rate']:.1f}% win rate, {row['signal_count']} signals, "
                      f"{row['avg_return']:.2f}% avg return, {row['max_adverse']:.2f}% max adverse")
        else:
            print("No combinations meet this criteria. Consider lowering thresholds.")


# This is the main execution block - runs when you execute this file directly
if __name__ == "__main__":
    print("=== XAUUSD MOMENTUM PERSISTENCE ANALYZER ===\n")
    
    # Initialize analyzer
    analyzer = XAUUSDMomentumAnalyzer()
    
    # Download data (you can also use analyzer.load_csv_data('your_file.csv'))
    analyzer.download_data(period="2y", interval="4h")
    
    # Run main analysis
    print("\nRunning momentum persistence analysis...")
    results = analyzer.analyze_momentum_persistence()
    
    # Find optimal thresholds
    print("\nFinding optimal combinations...")
    optimal = analyzer.find_optimal_thresholds(min_win_rate=75, min_signals=10)
    
    # Analyze by trading session
    print("\nAnalyzing by trading session...")
    session_analysis = analyzer.analyze_by_session(threshold=2.0, hours=24)
    print(session_analysis.round(2))
    
    # Generate plots and summary
    analyzer.plot_results()
    analyzer.summary_report()