#!/usr/bin/env python3
"""
Paper Trading Lessons Analyzer
Analyzes historical trade performance to provide data-driven recommendations
"""

import sqlite3
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent / "paper_trades.db"


class TradingLessonsAnalyzer:
    """Analyzes trade history to extract actionable lessons"""

    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path

    def get_performance_by_strategy(self) -> Dict[str, Dict]:
        """Analyze win rates and performance by strategy type"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                strategy,
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl_percent > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl_percent < 0 THEN 1 ELSE 0 END) as losses,
                AVG(pnl_percent) as avg_pnl,
                AVG(CASE WHEN pnl_percent > 0 THEN pnl_percent END) as avg_win,
                AVG(CASE WHEN pnl_percent < 0 THEN pnl_percent END) as avg_loss,
                SUM(pnl_usd) as total_pnl
            FROM paper_trades
            WHERE status IN ('CLOSED', 'STOPPED', 'TP2_HIT')
            AND strategy IS NOT NULL
            GROUP BY strategy
            HAVING COUNT(*) >= 3
        """)

        strategies = {}
        for row in cursor.fetchall():
            strategy = row['strategy']
            total = row['total_trades']
            wins = row['wins'] or 0
            win_rate = (wins / total * 100) if total > 0 else 0

            strategies[strategy] = {
                'total_trades': total,
                'wins': wins,
                'losses': row['losses'] or 0,
                'win_rate': win_rate,
                'avg_pnl': row['avg_pnl'],
                'avg_win': row['avg_win'],
                'avg_loss': row['avg_loss'],
                'total_pnl': row['total_pnl'],
                'recommendation': self._get_strategy_recommendation(win_rate, row['avg_pnl'])
            }

        conn.close()
        return strategies

    def get_performance_by_symbol(self) -> Dict[str, Dict]:
        """Analyze win rates and performance by symbol"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                symbol,
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl_percent > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl_percent < 0 THEN 1 ELSE 0 END) as losses,
                AVG(pnl_percent) as avg_pnl,
                SUM(pnl_usd) as total_pnl
            FROM paper_trades
            WHERE status IN ('CLOSED', 'STOPPED', 'TP2_HIT')
            GROUP BY symbol
            HAVING COUNT(*) >= 3
        """)

        symbols = {}
        for row in cursor.fetchall():
            symbol = row['symbol']
            total = row['total_trades']
            wins = row['wins'] or 0
            win_rate = (wins / total * 100) if total > 0 else 0

            symbols[symbol] = {
                'total_trades': total,
                'wins': wins,
                'losses': row['losses'] or 0,
                'win_rate': win_rate,
                'avg_pnl': row['avg_pnl'],
                'total_pnl': row['total_pnl'],
                'recommendation': self._get_symbol_recommendation(total, wins, row['total_pnl'])
            }

        conn.close()
        return symbols

    def get_account_health_metrics(self) -> Dict:
        """Calculate current account health for risk adjustment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl_percent > 0 THEN 1 ELSE 0 END) as wins,
                SUM(pnl_usd) as total_pnl_usd,
                AVG(CASE WHEN pnl_percent < 0 THEN pnl_percent END) as avg_loss_pct
            FROM paper_trades
            WHERE status IN ('CLOSED', 'STOPPED', 'TP2_HIT')
        """)

        row = cursor.fetchone()
        conn.close()

        if not row or row[0] == 0:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_pnl_pct': 0,
                'avg_loss_pct': 0,
                'risk_level': 'CONSERVATIVE',
                'max_position_size': 500,
                'required_rr': 4.0,
                'max_stop_pct': 1.0
            }

        total_trades = row[0]
        wins = row[1] or 0
        total_pnl_usd = row[2] or 0
        avg_loss_pct = abs(row[3] or 0)

        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        total_pnl_pct = (total_pnl_usd / (total_trades * 1000)) * 100  # Assuming $1000 per trade

        # Risk adjustment based on performance
        if total_pnl_pct < -20:  # Significant drawdown
            risk_level = 'ULTRA_CONSERVATIVE'
            max_position_size = 500
            required_rr = 5.0
            max_stop_pct = 0.75
        elif total_pnl_pct < -10:  # Moderate drawdown
            risk_level = 'CONSERVATIVE'
            max_position_size = 750
            required_rr = 4.0
            max_stop_pct = 1.0
        elif win_rate < 45:  # Low win rate
            risk_level = 'CONSERVATIVE'
            max_position_size = 800
            required_rr = 3.5
            max_stop_pct = 1.5
        else:  # Healthy account
            risk_level = 'NORMAL'
            max_position_size = 1000
            required_rr = 2.5
            max_stop_pct = 2.0

        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'total_pnl_pct': total_pnl_pct,
            'avg_loss_pct': avg_loss_pct,
            'risk_level': risk_level,
            'max_position_size': max_position_size,
            'required_rr': required_rr,
            'max_stop_pct': max_stop_pct
        }

    def get_recent_patterns(self, days: int = 7) -> Dict:
        """Analyze recent trading patterns for quick adjustments"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        cursor.execute("""
            SELECT
                COUNT(*) as recent_trades,
                SUM(CASE WHEN pnl_percent > 0 THEN 1 ELSE 0 END) as recent_wins,
                AVG(pnl_percent) as recent_avg_pnl,
                GROUP_CONCAT(symbol) as recent_symbols
            FROM paper_trades
            WHERE status IN ('CLOSED', 'STOPPED', 'TP2_HIT')
            AND exit_time >= ?
        """, (cutoff_date,))

        row = cursor.fetchone()
        conn.close()

        if not row or row['recent_trades'] == 0:
            return {'message': f'No trades in last {days} days'}

        recent_wins = row['recent_wins'] or 0
        recent_win_rate = (recent_wins / row['recent_trades'] * 100) if row['recent_trades'] > 0 else 0

        return {
            'recent_trades': row['recent_trades'],
            'recent_wins': recent_wins,
            'recent_win_rate': recent_win_rate,
            'recent_avg_pnl': row['recent_avg_pnl'],
            'trend': 'IMPROVING' if recent_win_rate > 50 else 'DECLINING'
        }

    def should_filter_opportunity(self, opportunity: Dict) -> Tuple[bool, str]:
        """
        Determine if an opportunity should be filtered out based on lessons learned
        Returns: (should_filter, reason)
        """
        symbol = opportunity.get('symbol', '').upper()
        strategy = opportunity.get('strategy', '')
        stop_loss_pct = abs(opportunity.get('stop_loss_percent', 0))
        rr_ratio = opportunity.get('risk_reward_ratio', 0)

        # Get performance data
        strategies = self.get_performance_by_strategy()
        symbols = self.get_performance_by_symbol()
        health = self.get_account_health_metrics()

        # Filter 1: Strategy with poor track record
        if strategy in strategies:
            strat_data = strategies[strategy]
            if strat_data['win_rate'] < 35 and strat_data['total_trades'] >= 5:
                return True, f"Strategy '{strategy}' has only {strat_data['win_rate']:.1f}% win rate ({strat_data['wins']}W/{strat_data['losses']}L). AVOID."

        # Filter 2: Symbol with poor performance
        if symbol in symbols:
            sym_data = symbols[symbol]
            if sym_data['wins'] == 0 and sym_data['total_trades'] >= 3:
                return True, f"{symbol} has 0 wins in {sym_data['total_trades']} trades. Total loss: ${sym_data['total_pnl']:.2f}. AVOID."
            if sym_data['win_rate'] < 30 and sym_data['total_trades'] >= 4:
                return True, f"{symbol} has poor {sym_data['win_rate']:.1f}% win rate. AVOID."

        # Filter 3: Stop loss too wide for current account health
        if stop_loss_pct > health['max_stop_pct']:
            return True, f"Stop loss {stop_loss_pct:.2f}% exceeds max {health['max_stop_pct']:.2f}% for {health['risk_level']} risk mode (account at {health['total_pnl_pct']:.1f}%)."

        # Filter 4: R:R ratio too low for account health
        if rr_ratio < health['required_rr']:
            return True, f"R:R {rr_ratio:.1f} below required {health['required_rr']:.1f} for {health['risk_level']} mode."

        return False, ""

    def get_enhanced_opportunity_context(self, opportunity: Dict) -> Dict:
        """Add historical context to an opportunity"""
        symbol = opportunity.get('symbol', '').upper()
        strategy = opportunity.get('strategy', '')

        strategies = self.get_performance_by_strategy()
        symbols = self.get_performance_by_symbol()

        context = {
            'strategy_history': None,
            'symbol_history': None,
            'confidence_adjustment': 0
        }

        # Add strategy history
        if strategy in strategies:
            strat_data = strategies[strategy]
            context['strategy_history'] = {
                'win_rate': strat_data['win_rate'],
                'total_trades': strat_data['total_trades'],
                'record': f"{strat_data['wins']}W/{strat_data['losses']}L",
                'avg_win': strat_data['avg_win'],
                'avg_loss': strat_data['avg_loss'],
                'recommendation': strat_data['recommendation']
            }

            # Adjust confidence based on historical performance
            if strat_data['win_rate'] > 65:
                context['confidence_adjustment'] += 1
            elif strat_data['win_rate'] < 45:
                context['confidence_adjustment'] -= 2

        # Add symbol history
        if symbol in symbols:
            sym_data = symbols[symbol]
            context['symbol_history'] = {
                'win_rate': sym_data['win_rate'],
                'total_trades': sym_data['total_trades'],
                'record': f"{sym_data['wins']}W/{sym_data['losses']}L",
                'total_pnl': sym_data['total_pnl'],
                'recommendation': sym_data['recommendation']
            }

            # Adjust confidence based on symbol performance
            if sym_data['wins'] == 0 and sym_data['total_trades'] >= 2:
                context['confidence_adjustment'] -= 3
            elif sym_data['win_rate'] > 60:
                context['confidence_adjustment'] += 1

        return context

    def get_lessons_summary(self) -> Dict:
        """Generate comprehensive lessons learned summary"""
        strategies = self.get_performance_by_strategy()
        symbols = self.get_performance_by_symbol()
        health = self.get_account_health_metrics()
        recent = self.get_recent_patterns(7)

        # Identify worst strategies
        worst_strategies = [
            (name, data) for name, data in strategies.items()
            if data['win_rate'] < 40 and data['total_trades'] >= 3
        ]
        worst_strategies.sort(key=lambda x: x[1]['win_rate'])

        # Identify best strategies
        best_strategies = [
            (name, data) for name, data in strategies.items()
            if data['win_rate'] > 55 and data['total_trades'] >= 3
        ]
        best_strategies.sort(key=lambda x: x[1]['win_rate'], reverse=True)

        # Identify problem symbols
        problem_symbols = [
            (name, data) for name, data in symbols.items()
            if (data['wins'] == 0 and data['total_trades'] >= 2) or
               (data['win_rate'] < 35 and data['total_trades'] >= 3)
        ]

        return {
            'account_health': health,
            'recent_performance': recent,
            'worst_strategies': worst_strategies[:3],
            'best_strategies': best_strategies[:3],
            'problem_symbols': problem_symbols,
            'total_strategies_analyzed': len(strategies),
            'total_symbols_analyzed': len(symbols)
        }

    @staticmethod
    def _get_strategy_recommendation(win_rate: float, avg_pnl: float) -> str:
        """Get recommendation for a strategy"""
        if win_rate >= 60 and avg_pnl > 1.0:
            return "EXCELLENT - Prioritize this strategy"
        elif win_rate >= 50 and avg_pnl > 0:
            return "GOOD - Continue using"
        elif win_rate >= 40:
            return "NEUTRAL - Use with caution"
        else:
            return "POOR - Avoid this strategy"

    @staticmethod
    def _get_symbol_recommendation(total_trades: int, wins: int, total_pnl: float) -> str:
        """Get recommendation for a symbol"""
        if wins == 0 and total_trades >= 3:
            return "AVOID - 0% win rate"
        elif total_pnl < -50 and total_trades >= 3:
            return "AVOID - Heavy losses"
        elif wins / total_trades > 0.6:
            return "FAVORABLE - Good track record"
        else:
            return "NEUTRAL - Mixed results"


def get_analyzer() -> TradingLessonsAnalyzer:
    """Convenience function to get analyzer instance"""
    return TradingLessonsAnalyzer()


if __name__ == "__main__":
    # Test the analyzer
    analyzer = TradingLessonsAnalyzer()

    print("=" * 60)
    print("PAPER TRADING LESSONS ANALYSIS")
    print("=" * 60)

    # Account health
    health = analyzer.get_account_health_metrics()
    print(f"\nACCOUNT HEALTH:")
    print(f"Risk Level: {health['risk_level']}")
    print(f"Win Rate: {health['win_rate']:.1f}%")
    print(f"Total P&L: {health['total_pnl_pct']:.1f}%")
    print(f"Max Position Size: ${health['max_position_size']}")
    print(f"Required R:R: {health['required_rr']:.1f}")
    print(f"Max Stop Loss: {health['max_stop_pct']:.1f}%")

    # Lessons summary
    lessons = analyzer.get_lessons_summary()

    print(f"\nWORST STRATEGIES (Avoid These):")
    for name, data in lessons['worst_strategies']:
        print(f"  - {name}: {data['win_rate']:.1f}% win rate ({data['wins']}W/{data['losses']}L)")

    print(f"\nBEST STRATEGIES (Prioritize These):")
    for name, data in lessons['best_strategies']:
        print(f"  - {name}: {data['win_rate']:.1f}% win rate ({data['wins']}W/{data['losses']}L)")

    print(f"\nPROBLEM SYMBOLS (Avoid):")
    for name, data in lessons['problem_symbols']:
        print(f"  - {name}: {data['win_rate']:.1f}% win rate ({data['wins']}W/{data['losses']}L), P&L: ${data['total_pnl']:.2f}")

    print(f"\nRECENT PERFORMANCE (Last 7 days):")
    if 'message' in lessons['recent_performance']:
        print(f"  {lessons['recent_performance']['message']}")
    else:
        rp = lessons['recent_performance']
        print(f"  Trades: {rp['recent_trades']}")
        print(f"  Win Rate: {rp['recent_win_rate']:.1f}%")
        print(f"  Trend: {rp['trend']}")

    print("\n" + "=" * 60)
