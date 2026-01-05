"""
Technical Indicator Signal Calculators
Each function calculates a rating (-3 to +3) and signal for a specific indicator.
All thresholds are imported from trading_constants.py for easy tuning.
"""

from __future__ import annotations
from typing import Tuple, Optional
import logging

from trading_constants import (
    Signal,
    STOCH_OVERSOLD, STOCH_EXTREMELY_OVERSOLD,
    STOCH_OVERBOUGHT, STOCH_EXTREMELY_OVERBOUGHT, STOCH_MIDPOINT,
    MACD_HIST_MODERATE, MACD_HIST_STRONG, MACD_ZERO_LINE,
    ADX_WEAK_TREND, ADX_TREND_THRESHOLD, ADX_STRONG_TREND, ADX_VERY_STRONG_TREND,
    CCI_MILDLY_BEARISH, CCI_OVERBOUGHT, CCI_EXTREMELY_OVERBOUGHT,
    CCI_MILDLY_BULLISH, CCI_OVERSOLD, CCI_EXTREMELY_OVERSOLD,
    BB_POSITION_THRESHOLD,
    RATING_MAX, RATING_MIN,
)

logger = logging.getLogger(__name__)


def compute_change(open_price: float, close: float) -> float:
    """
    Calculate percentage change from open to close price.
    
    Args:
        open_price: Opening price
        close: Closing price
    
    Returns:
        Percentage change (e.g., 2.5 for 2.5% increase)
    """
    if open_price is None or open_price == 0:
        logger.warning(f"Invalid open_price: {open_price}, returning 0.0")
        return 0.0
    return ((close - open_price) / open_price) * 100


def compute_bbw(sma: float, bb_upper: float, bb_lower: float) -> Optional[float]:
    """
    Calculate Bollinger Band Width (BBW).
    BBW = (Upper Band - Lower Band) / Middle Band (SMA)
    
    Args:
        sma: Simple Moving Average (middle band)
        bb_upper: Upper Bollinger Band
        bb_lower: Lower Bollinger Band
    
    Returns:
        BBW value or None if SMA is invalid
    """
    # FIXED: Proper validation instead of "if not sma"
    if sma is None or sma == 0:
        return None
    
    try:
        return (bb_upper - bb_lower) / sma
    except (TypeError, ZeroDivisionError):
        logger.error(f"Error calculating BBW: sma={sma}, upper={bb_upper}, lower={bb_lower}")
        return None


def compute_bb_rating_signal(
    close: float, bb_upper: float, bb_middle: float, bb_lower: float
) -> Tuple[int, str]:
    """
    Calculate Bollinger Bands rating and signal.
    
    Strategy: Mean reversion
    - Price near/above upper band → Overbought → Potential sell
    - Price near/below lower band → Oversold → Potential buy
    
    Rating scale:
        +3: Far above upper band (extremely overbought)
        +2: Above upper band (overbought) → SELL signal
        +1: In upper half of bands
         0: At middle band
        -1: In lower half of bands
        -2: Below lower band (oversold) → BUY signal
        -3: Far below lower band (extremely oversold)
    
    Args:
        close: Current closing price
        bb_upper: Upper Bollinger Band
        bb_middle: Middle Bollinger Band (SMA)
        bb_lower: Lower Bollinger Band
    
    Returns:
        Tuple of (rating, signal)
    """
    rating = 0
    
    upper_half_threshold = bb_middle + ((bb_upper - bb_middle) * BB_POSITION_THRESHOLD)
    lower_half_threshold = bb_middle - ((bb_middle - bb_lower) * BB_POSITION_THRESHOLD)
    
    if close > bb_upper:
        rating = 3  # Extremely overbought
    elif close > upper_half_threshold:
        rating = 2  # Overbought
    elif close > bb_middle:
        rating = 1  # Mildly bullish
    elif close < bb_lower:
        rating = -3  # Extremely oversold
    elif close < lower_half_threshold:
        rating = -2  # Oversold
    elif close < bb_middle:
        rating = -1  # Mildly bearish
    
    # Mean reversion strategy: Overbought → Sell, Oversold → Buy
    signal = Signal.NEUTRAL
    if rating == 3:
        signal = Signal.STRONG_SELL  # Extremely overbought
    elif rating == 2:
        signal = Signal.SELL  # Overbought
    elif rating == -2:
        signal = Signal.BUY  # Oversold
    elif rating == -3:
        signal = Signal.STRONG_BUY  # Extremely oversold
    
    return rating, signal.value


def compute_stoch_rsi_signal(stoch_k: float, stoch_d: float) -> Tuple[int, str]:
    """
    Calculate Stochastic RSI signal.
    
    Strategy: Momentum oscillator
    - Oversold (< 20): Bullish signal
    - Overbought (> 80): Bearish signal
    - Crossovers: K crossing D adds conviction
    
    Args:
        stoch_k: Stochastic RSI K line (0-100)
        stoch_d: Stochastic RSI D line (0-100)
    
    Returns:
        Tuple of (rating, signal)
    """
    rating = 0
    
    # Base rating from overbought/oversold levels
    if stoch_k < STOCH_EXTREMELY_OVERSOLD:
        rating = -3  # Extremely oversold → Strong buy
    elif stoch_k < STOCH_OVERSOLD:
        rating = -2  # Oversold → Buy
    elif stoch_k > STOCH_EXTREMELY_OVERBOUGHT:
        rating = 3  # Extremely overbought → Strong sell
    elif stoch_k > STOCH_OVERBOUGHT:
        rating = 2  # Overbought → Sell
    
    # Crossover signals (adds conviction)
    if stoch_k > stoch_d and stoch_k < STOCH_MIDPOINT:
        # Bullish crossover in lower region
        rating = max(rating - 1, RATING_MIN)
    elif stoch_k < stoch_d and stoch_k > STOCH_MIDPOINT:
        # Bearish crossover in upper region
        rating = min(rating + 1, RATING_MAX)
    
    # Generate signal
    signal = Signal.NEUTRAL
    if rating <= -3:
        signal = Signal.STRONG_BUY
    elif rating == -2:
        signal = Signal.BUY
    elif rating >= 3:
        signal = Signal.STRONG_SELL
    elif rating == 2:
        signal = Signal.SELL
    
    return rating, signal.value


def compute_macd_signal(macd: float, macd_signal_line: float, macd_histogram: float) -> Tuple[int, str]:
    """
    Calculate MACD signal.
    
    Strategy: Trend following with momentum
    - MACD > Signal: Bullish
    - MACD < Signal: Bearish
    - Histogram strength adds conviction
    
    Args:
        macd: MACD line
        macd_signal_line: Signal line
        macd_histogram: MACD histogram (MACD - Signal)
    
    Returns:
        Tuple of (rating, signal)
    """
    rating = 0
    
    # Basic crossover with histogram strength
    if macd > macd_signal_line:
        # Bullish - check histogram strength (larger threshold first)
        if macd_histogram > MACD_HIST_STRONG:
            rating = -3  # Strong bullish momentum
        elif macd_histogram > MACD_HIST_MODERATE:
            rating = -2  # Moderate bullish momentum
        else:
            rating = -1  # Weak bullish signal
    elif macd < macd_signal_line:
        # Bearish - check histogram strength
        if macd_histogram < -MACD_HIST_STRONG:
            rating = 3  # Strong bearish momentum
        elif macd_histogram < -MACD_HIST_MODERATE:
            rating = 2  # Moderate bearish momentum
        else:
            rating = 1  # Weak bearish signal
    
    # Generate signal
    signal = Signal.NEUTRAL
    if rating <= -3:
        signal = Signal.STRONG_BUY
    elif rating == -2:
        signal = Signal.BUY
    elif rating == -1:
        signal = Signal.BUY  # Weak buy still counts as buy
    elif rating == 1:
        signal = Signal.SELL  # Weak sell still counts as sell
    elif rating == 2:
        signal = Signal.SELL
    elif rating >= 3:
        signal = Signal.STRONG_SELL
    
    return rating, signal.value


def compute_adx_signal(adx: float, plus_di: float, minus_di: float) -> Tuple[int, str, float]:
    """
    Calculate ADX (Average Directional Index) signal.
    
    Strategy: Trend strength indicator
    - ADX > 25: Strong trend
    - ADX < 20: Weak/no trend
    - +DI vs -DI determines direction
    
    Args:
        adx: ADX value (0-100)
        plus_di: Plus Directional Indicator
        minus_di: Minus Directional Indicator
    
    Returns:
        Tuple of (rating, signal, trend_strength)
    """
    # Calculate trend strength (0.0 to 1.0)
    if adx > ADX_VERY_STRONG_TREND:
        trend_strength = 1.0  # Very strong trend
    elif adx > ADX_STRONG_TREND:
        trend_strength = 0.85  # Strong trend
    elif adx > ADX_TREND_THRESHOLD:
        trend_strength = 0.7  # Moderate trend
    elif adx > ADX_WEAK_TREND:
        trend_strength = 0.4  # Weak trend
    else:
        trend_strength = 0.2  # Very weak/no trend
    
    rating = 0
    
    # Determine direction and strength
    if plus_di > minus_di:
        # Bullish trend
        if adx > ADX_STRONG_TREND:
            rating = -3  # Strong bullish trend
        elif adx > ADX_TREND_THRESHOLD:
            rating = -2  # Moderate bullish trend
        else:
            rating = -1  # Weak bullish trend
    elif minus_di > plus_di:
        # Bearish trend
        if adx > ADX_STRONG_TREND:
            rating = 3  # Strong bearish trend
        elif adx > ADX_TREND_THRESHOLD:
            rating = 2  # Moderate bearish trend
        else:
            rating = 1  # Weak bearish trend
    
    # Generate signal
    signal = Signal.NEUTRAL
    if rating <= -3:
        signal = Signal.STRONG_BUY
    elif rating == -2:
        signal = Signal.BUY
    elif rating >= 3:
        signal = Signal.STRONG_SELL
    elif rating == 2:
        signal = Signal.SELL
    
    return rating, signal.value, trend_strength


def compute_cci_signal(cci: float) -> Tuple[int, str]:
    """
    Calculate CCI (Commodity Channel Index) signal.
    
    Strategy: Mean reversion oscillator
    - > +100: Overbought → Sell signal
    - < -100: Oversold → Buy signal
    - Extreme levels (+/-200): Strong signals
    
    Args:
        cci: CCI value (typically -300 to +300, but can exceed)
    
    Returns:
        Tuple of (rating, signal)
    """
    rating = 0
    
    if cci > CCI_EXTREMELY_OVERBOUGHT:
        rating = 3  # Extremely overbought → Strong sell
    elif cci > CCI_OVERBOUGHT:
        rating = 2  # Overbought → Sell
    elif cci > CCI_MILDLY_BEARISH:
        rating = 1  # Mildly overbought
    elif cci < CCI_EXTREMELY_OVERSOLD:
        rating = -3  # Extremely oversold → Strong buy
    elif cci < CCI_OVERSOLD:
        rating = -2  # Oversold → Buy
    elif cci < CCI_MILDLY_BULLISH:
        rating = -1  # Mildly oversold
    
    # Generate signal (mean reversion)
    signal = Signal.NEUTRAL
    if rating <= -3:
        signal = Signal.STRONG_BUY
    elif rating == -2:
        signal = Signal.BUY
    elif rating >= 3:
        signal = Signal.STRONG_SELL
    elif rating == 2:
        signal = Signal.SELL
    
    return rating, signal.value
