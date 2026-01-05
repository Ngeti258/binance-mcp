"""
Trading Constants and Thresholds
All magic numbers extracted to constants for easy tuning and maintenance.
"""

from enum import Enum


class Signal(str, Enum):
    """Trading signal types"""
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    NEUTRAL = "NEUTRAL"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


# ==================== STOCHASTIC RSI THRESHOLDS ====================
STOCH_OVERSOLD = 20.0
STOCH_EXTREMELY_OVERSOLD = 10.0
STOCH_OVERBOUGHT = 80.0
STOCH_EXTREMELY_OVERBOUGHT = 90.0
STOCH_MIDPOINT = 50.0

# Valid range for Stochastic RSI
STOCH_MIN = 0.0
STOCH_MAX = 100.0


# ==================== MACD THRESHOLDS ====================
MACD_HIST_MODERATE = 0.5
MACD_HIST_STRONG = 1.0
MACD_ZERO_LINE = 0.0


# ==================== ADX THRESHOLDS ====================
ADX_WEAK_TREND = 20.0
ADX_TREND_THRESHOLD = 25.0
ADX_STRONG_TREND = 40.0
ADX_VERY_STRONG_TREND = 50.0

# Valid range for ADX
ADX_MIN = 0.0
ADX_MAX = 100.0


# ==================== CCI THRESHOLDS ====================
CCI_MILDLY_BEARISH = 50.0
CCI_OVERBOUGHT = 100.0
CCI_EXTREMELY_OVERBOUGHT = 200.0
CCI_MILDLY_BULLISH = -50.0
CCI_OVERSOLD = -100.0
CCI_EXTREMELY_OVERSOLD = -200.0

# Typical CCI range (can exceed these)
CCI_TYPICAL_MIN = -300.0
CCI_TYPICAL_MAX = 300.0


# ==================== BOLLINGER BANDS ====================
BB_POSITION_THRESHOLD = 0.5  # Threshold for upper/lower half of bands


# ==================== RATING SCALE ====================
RATING_MIN = -3
RATING_MAX = 3
RATING_NEUTRAL = 0


# ==================== DEFAULT INDICATOR WEIGHTS ====================
DEFAULT_WEIGHTS = {
    "bb": 1.0,
    "stoch_rsi": 1.2,  # Slightly higher weight for momentum
    "macd": 1.0,
    "adx": 0.8,  # ADX is more for trend confirmation
    "cci": 1.0,
}


# ==================== TREND STRENGTH THRESHOLDS ====================
TREND_STRENGTH_WEAK = 0.3
TREND_STRENGTH_MODERATE = 0.6


# ==================== PRICE VALIDATION ====================
MIN_VALID_PRICE = 0.0  # Prices must be positive
