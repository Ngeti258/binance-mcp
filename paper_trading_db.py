#!/usr/bin/env python3
"""
Paper Trading Database Manager
Handles all database operations for paper trading system
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

DB_PATH = Path(__file__).parent / "paper_trades.db"

class PaperTradingDB:
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.executescript("""
        -- Paper Trading Trades Table
        CREATE TABLE IF NOT EXISTS paper_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_id TEXT UNIQUE NOT NULL,

            -- Trade Details
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            strategy TEXT,
            timeframe TEXT DEFAULT '1h',

            -- Entry
            entry_time TIMESTAMP NOT NULL,
            entry_price_usd REAL NOT NULL,
            entry_price_kes REAL NOT NULL,
            position_size_usd REAL DEFAULT 1000,

            -- Risk Management
            stop_loss_usd REAL NOT NULL,
            stop_loss_kes REAL NOT NULL,
            stop_loss_percent REAL,
            target1_usd REAL NOT NULL,
            target1_kes REAL NOT NULL,
            target1_percent REAL,
            target2_usd REAL,
            target2_kes REAL,
            target2_percent REAL,
            risk_reward_ratio REAL,

            -- Status
            status TEXT DEFAULT 'OPEN',

            -- Exit
            exit_time TIMESTAMP,
            exit_price_usd REAL,
            exit_price_kes REAL,
            exit_reason TEXT,

            -- Performance
            pnl_usd REAL,
            pnl_kes REAL,
            pnl_percent REAL,
            max_favorable_excursion REAL,
            max_adverse_excursion REAL,

            -- Context
            analysis_snapshot TEXT,
            rationale TEXT,
            market_context TEXT,

            -- Metadata
            created_by TEXT DEFAULT 'claude_majors',
            notes TEXT
        );

        -- Trade History Log
        CREATE TABLE IF NOT EXISTS trade_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_id TEXT NOT NULL,
            check_time TIMESTAMP NOT NULL,
            current_price_usd REAL NOT NULL,
            current_price_kes REAL NOT NULL,
            unrealized_pnl_percent REAL,
            status_at_check TEXT,
            FOREIGN KEY (trade_id) REFERENCES paper_trades(trade_id)
        );

        -- Strategy Performance Tracking
        CREATE TABLE IF NOT EXISTS strategy_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_name TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            total_trades INTEGER DEFAULT 0,
            winning_trades INTEGER DEFAULT 0,
            losing_trades INTEGER DEFAULT 0,
            total_pnl_usd REAL DEFAULT 0,
            avg_pnl_percent REAL,
            win_rate REAL,
            avg_risk_reward REAL,
            sharpe_ratio REAL,
            max_drawdown REAL,
            last_updated TIMESTAMP,
            UNIQUE(strategy_name, timeframe)
        );

        -- Learning Database
        CREATE TABLE IF NOT EXISTS trade_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight_date TIMESTAMP,
            insight_type TEXT,
            description TEXT,
            trades_analyzed INTEGER,
            confidence_score REAL,
            actionable_rule TEXT
        );
        """)

        conn.commit()
        conn.close()

    def create_trade(self, trade_data: Dict) -> str:
        """Create new paper trade"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        trade_id = f"{trade_data['symbol']}_{trade_data['side']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        cursor.execute("""
            INSERT INTO paper_trades (
                trade_id, symbol, side, strategy, timeframe,
                entry_time, entry_price_usd, entry_price_kes,
                position_size_usd, stop_loss_usd, stop_loss_kes,
                stop_loss_percent, target1_usd, target1_kes,
                target1_percent, target2_usd, target2_kes,
                target2_percent, risk_reward_ratio,
                analysis_snapshot, rationale, market_context
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade_id, trade_data['symbol'], trade_data['side'],
            trade_data.get('strategy'), trade_data.get('timeframe', '1h'),
            datetime.utcnow(), trade_data['entry_price_usd'], trade_data['entry_price_kes'],
            trade_data.get('position_size_usd', 1000),
            trade_data['stop_loss_usd'], trade_data['stop_loss_kes'],
            trade_data.get('stop_loss_percent'),
            trade_data['target1_usd'], trade_data['target1_kes'],
            trade_data.get('target1_percent'),
            trade_data.get('target2_usd'), trade_data.get('target2_kes'),
            trade_data.get('target2_percent'),
            trade_data.get('risk_reward_ratio'),
            json.dumps(trade_data.get('analysis_snapshot')) if trade_data.get('analysis_snapshot') else None,
            trade_data.get('rationale'),
            trade_data.get('market_context')
        ))

        conn.commit()
        conn.close()
        return trade_id

    def get_open_trades(self) -> List[Dict]:
        """Get all open trades"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM paper_trades
            WHERE status IN ('OPEN', 'TP1_HIT')
            ORDER BY entry_time DESC
        """)

        trades = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return trades

    def update_trade_check(self, trade_id: str, current_price_usd: float,
                          current_price_kes: float) -> Dict:
        """
        Check trade against current price and update status
        Returns updated trade status
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get trade
        cursor.execute("SELECT * FROM paper_trades WHERE trade_id = ?", (trade_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return {'error': f'Trade {trade_id} not found'}

        trade = dict(row)

        if trade['status'] in ('CLOSED', 'STOPPED', 'TP2_HIT'):
            conn.close()
            return trade

        # Calculate unrealized P&L
        entry = trade['entry_price_usd']
        if trade['side'] == 'LONG':
            pnl_percent = ((current_price_usd - entry) / entry) * 100
        else:  # SHORT
            pnl_percent = ((entry - current_price_usd) / entry) * 100

        # Check stop loss
        new_status = trade['status']

        if trade['side'] == 'LONG' and current_price_usd <= trade['stop_loss_usd']:
            self._close_trade(cursor, trade_id, current_price_usd, current_price_kes,
                            'STOP_LOSS', pnl_percent)
            new_status = 'STOPPED'
        elif trade['side'] == 'SHORT' and current_price_usd >= trade['stop_loss_usd']:
            self._close_trade(cursor, trade_id, current_price_usd, current_price_kes,
                            'STOP_LOSS', pnl_percent)
            new_status = 'STOPPED'

        # Check targets
        elif trade['side'] == 'LONG':
            if trade.get('target2_usd') and current_price_usd >= trade['target2_usd']:
                self._close_trade(cursor, trade_id, current_price_usd, current_price_kes,
                                'TARGET2', pnl_percent)
                new_status = 'TP2_HIT'
            elif current_price_usd >= trade['target1_usd'] and trade['status'] != 'TP1_HIT':
                cursor.execute("UPDATE paper_trades SET status = 'TP1_HIT' WHERE trade_id = ?", (trade_id,))
                new_status = 'TP1_HIT'
        else:  # SHORT
            if trade.get('target2_usd') and current_price_usd <= trade['target2_usd']:
                self._close_trade(cursor, trade_id, current_price_usd, current_price_kes,
                                'TARGET2', pnl_percent)
                new_status = 'TP2_HIT'
            elif current_price_usd <= trade['target1_usd'] and trade['status'] != 'TP1_HIT':
                cursor.execute("UPDATE paper_trades SET status = 'TP1_HIT' WHERE trade_id = ?", (trade_id,))
                new_status = 'TP1_HIT'

        # Log trade check
        cursor.execute("""
            INSERT INTO trade_checks (trade_id, check_time, current_price_usd,
                                     current_price_kes, unrealized_pnl_percent, status_at_check)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (trade_id, datetime.utcnow(), current_price_usd, current_price_kes,
              pnl_percent, new_status))

        # Update max favorable/adverse excursion
        current_mfe = trade.get('max_favorable_excursion') or 0
        current_mae = trade.get('max_adverse_excursion') or 0

        if pnl_percent > current_mfe:
            cursor.execute("""
                UPDATE paper_trades
                SET max_favorable_excursion = ?
                WHERE trade_id = ?
            """, (pnl_percent, trade_id))

        if pnl_percent < current_mae:
            cursor.execute("""
                UPDATE paper_trades
                SET max_adverse_excursion = ?
                WHERE trade_id = ?
            """, (pnl_percent, trade_id))

        conn.commit()
        conn.close()

        return {
            'trade_id': trade_id,
            'symbol': trade['symbol'],
            'side': trade['side'],
            'status': new_status,
            'entry_price_usd': trade['entry_price_usd'],
            'current_price_usd': current_price_usd,
            'unrealized_pnl_percent': pnl_percent,
            'stop_loss_usd': trade['stop_loss_usd'],
            'target1_usd': trade['target1_usd'],
            'target2_usd': trade.get('target2_usd')
        }

    def _close_trade(self, cursor, trade_id: str, exit_price_usd: float,
                     exit_price_kes: float, exit_reason: str, pnl_percent: float):
        """Close a trade"""
        # Calculate P&L in USD
        cursor.execute("SELECT position_size_usd FROM paper_trades WHERE trade_id = ?", (trade_id,))
        position_size = cursor.fetchone()[0]
        pnl_usd = position_size * (pnl_percent / 100)
        pnl_kes = pnl_usd * (exit_price_kes / exit_price_usd)

        cursor.execute("""
            UPDATE paper_trades
            SET status = 'CLOSED',
                exit_time = ?,
                exit_price_usd = ?,
                exit_price_kes = ?,
                exit_reason = ?,
                pnl_percent = ?,
                pnl_usd = ?,
                pnl_kes = ?
            WHERE trade_id = ?
        """, (datetime.utcnow(), exit_price_usd, exit_price_kes,
              exit_reason, pnl_percent, pnl_usd, pnl_kes, trade_id))

    def manually_close_trade(self, trade_id: str, exit_price_usd: float,
                            exit_price_kes: float, reason: str = "MANUAL_CLOSE") -> bool:
        """Manually close a trade"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM paper_trades WHERE trade_id = ?", (trade_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return False

        trade = dict(row)
        entry = trade['entry_price_usd']

        if trade['side'] == 'LONG':
            pnl_percent = ((exit_price_usd - entry) / entry) * 100
        else:
            pnl_percent = ((entry - exit_price_usd) / entry) * 100

        self._close_trade(cursor, trade_id, exit_price_usd, exit_price_kes, reason, pnl_percent)

        conn.commit()
        conn.close()
        return True

    def get_trade_history(self, limit: int = 50) -> List[Dict]:
        """Get closed trade history"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM paper_trades
            WHERE status IN ('CLOSED', 'STOPPED', 'TP2_HIT')
            ORDER BY exit_time DESC
            LIMIT ?
        """, (limit,))

        trades = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return trades

    def get_strategy_stats(self) -> Optional[Dict]:
        """Calculate overall strategy performance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl_percent > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl_percent < 0 THEN 1 ELSE 0 END) as losses,
                AVG(pnl_percent) as avg_pnl,
                AVG(CASE WHEN pnl_percent > 0 THEN pnl_percent END) as avg_win,
                AVG(CASE WHEN pnl_percent < 0 THEN pnl_percent END) as avg_loss,
                MAX(pnl_percent) as best_trade,
                MIN(pnl_percent) as worst_trade,
                SUM(pnl_usd) as total_pnl_usd
            FROM paper_trades
            WHERE status IN ('CLOSED', 'STOPPED', 'TP2_HIT')
        """)

        row = cursor.fetchone()
        conn.close()

        if row[0] == 0:  # No trades
            return None

        win_rate = (row[1] / row[0] * 100) if row[0] > 0 else 0

        return {
            'total_trades': row[0],
            'wins': row[1],
            'losses': row[2],
            'win_rate': win_rate,
            'avg_pnl_percent': row[3],
            'avg_win_percent': row[4],
            'avg_loss_percent': row[5],
            'best_trade_percent': row[6],
            'worst_trade_percent': row[7],
            'total_pnl_usd': row[8]
        }

    def get_trade_by_id(self, trade_id: str) -> Optional[Dict]:
        """Get a specific trade by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM paper_trades WHERE trade_id = ?", (trade_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None


# Convenience function for easy import
def get_db() -> PaperTradingDB:
    """Get paper trading database instance"""
    return PaperTradingDB()


if __name__ == "__main__":
    # Test database initialization
    db = PaperTradingDB()
    print("[OK] Paper trading database initialized successfully!")
    print(f"[INFO] Database location: {DB_PATH}")

    # Test stats (should return None for empty DB)
    stats = db.get_strategy_stats()
    if stats is None:
        print("[INFO] No trades yet - database is ready for first trade!")
    else:
        print(f"[STATS] Strategy Stats: {stats}")
