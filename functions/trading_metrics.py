"""
Main Trading Metrics Calculator
Combines all technical indicators into a comprehensive trading signal.
Includes input validation and proper error handling.
"""

from __future__ import annotations
from typing import Dict, Optional, List, Tuple
import logging

from trading_constants import (
    Signal, DEFAULT_WEIGHTS,
    STOCH_MIN, STOCH_MAX,
    ADX_MIN, ADX_MAX,
    CCI_TYPICAL_MIN, CCI_TYPICAL_MAX,
    MIN_VALID_PRICE,
    RATING_MAX, RATING_MIN,
)
from trading_indicators import (
    compute_change, compute_bbw,
    compute_bb_rating_signal,
    compute_stoch_rsi_signal,
    compute_macd_signal,
    compute_adx_signal,
    compute_cci_signal,
)

logger = logging.getLogger(__name__)


def validate_indicators(indicators: Dict) -> None:
    """
    Validate that all required indicators are present and have valid values.
    
    Args:
        indicators: Dictionary of indicator values
    
    Raises:
        KeyError: If required indicators are missing
        ValueError: If indicator values are invalid
    """
    # Check required keys
    required_keys = [
        "open", "close",
        "SMA20", "BB.upper", "BB.lower",
        "StochRSI.K", "StochRSI.D",
        "MACD", "MACD.signal", "MACD.histogram",
        "ADX", "ADX.plus_di", "ADX.minus_di",
        "CCI",
    ]
    
    missing_keys = [key for key in required_keys if key not in indicators]
    if missing_keys:
        raise KeyError(f"Missing required indicators: {missing_keys}")
    
    # Validate price data
    open_price = indicators["open"]
    close = indicators["close"]
    
    if open_price is None or close is None:
        raise ValueError("Price data cannot be None")
    
    if open_price <= MIN_VALID_PRICE or close <= MIN_VALID_PRICE:
        raise ValueError(f"Invalid prices: open={open_price}, close={close}. Prices must be positive.")
    
    # Validate Bollinger Bands
    bb_upper = indicators["BB.upper"]
    bb_lower = indicators["BB.lower"]
    sma = indicators["SMA20"]
    
    if bb_upper <= bb_lower:
        raise ValueError(f"Invalid Bollinger Bands: upper={bb_upper} must be > lower={bb_lower}")
    
    if sma is not None and not (bb_lower <= sma <= bb_upper):
        logger.warning(f"SMA ({sma}) is outside Bollinger Bands [{bb_lower}, {bb_upper}]")
    
    # Validate Stochastic RSI (must be 0-100)
    stoch_k = indicators["StochRSI.K"]
    stoch_d = indicators["StochRSI.D"]
    
    if not (STOCH_MIN <= stoch_k <= STOCH_MAX):
        raise ValueError(f"StochRSI.K out of range: {stoch_k} (must be {STOCH_MIN}-{STOCH_MAX})")
    
    if not (STOCH_MIN <= stoch_d <= STOCH_MAX):
        raise ValueError(f"StochRSI.D out of range: {stoch_d} (must be {STOCH_MIN}-{STOCH_MAX})")
    
    # Validate ADX (must be 0-100)
    adx = indicators["ADX"]
    
    if not (ADX_MIN <= adx <= ADX_MAX):
        raise ValueError(f"ADX out of range: {adx} (must be {ADX_MIN}-{ADX_MAX})")
    
    # Validate CCI (warn if outside typical range)
    cci = indicators["CCI"]
    
    if cci < CCI_TYPICAL_MIN or cci > CCI_TYPICAL_MAX:
        logger.warning(f"CCI value {cci} is outside typical range [{CCI_TYPICAL_MIN}, {CCI_TYPICAL_MAX}]")


def compute_composite_signal(ratings: List[Tuple[str, int, float]]) -> Tuple[int, str, Dict]:
    """
    Calculate composite signal from all indicators using weighted average.
    
    Args:
        ratings: List of (indicator_name, rating, weight) tuples
    
    Returns:
        Tuple of (composite_rating, composite_signal, breakdown)
    """
    if not ratings:
        return 0, Signal.NEUTRAL.value, {}
    
    # Calculate weighted average
    weighted_sum = sum(rating * weight for _, rating, weight in ratings)
    total_weight = sum(weight for _, _, weight in ratings)
    
    raw_score = weighted_sum / total_weight if total_weight else 0
    composite_rating = round(raw_score)
    
    # Cap rating at min/max
    composite_rating = max(RATING_MIN, min(RATING_MAX, composite_rating))
    
    # Generate signal
    signal = Signal.NEUTRAL
    if composite_rating <= -3:
        signal = Signal.STRONG_BUY
    elif composite_rating == -2:
        signal = Signal.BUY
    elif composite_rating == -1:
        signal = Signal.BUY  # Lean bullish
    elif composite_rating == 1:
        signal = Signal.SELL  # Lean bearish
    elif composite_rating == 2:
        signal = Signal.SELL
    elif composite_rating >= 3:
        signal = Signal.STRONG_SELL
    
    # Create breakdown
    breakdown = {
        "raw_score": round(raw_score, 2),
        "weighted_score": round(raw_score, 2),
        "bullish_indicators": sum(1 for _, r, _ in ratings if r < 0),  # Negative rating = bullish
        "bearish_indicators": sum(1 for _, r, _ in ratings if r > 0),  # Positive rating = bearish
        "neutral_indicators": sum(1 for _, r, _ in ratings if r == 0),
        "total_indicators": len(ratings),
    }
    
    return composite_rating, signal.value, breakdown


def compute_metrics(
    indicators: Dict,
    weights: Optional[Dict[str, float]] = None,
    validate: bool = True
) -> Optional[Dict]:
    """
    Calculate comprehensive trading metrics from multiple technical indicators.
    
    Args:
        indicators: Dictionary containing all indicator values
        weights: Optional custom weights for each indicator (default: equal weight)
        validate: Whether to validate input data (default: True)
    
    Required indicator keys:
        - open, close: Price data
        - SMA20, BB.upper, BB.lower: Bollinger Bands
        - StochRSI.K, StochRSI.D: Stochastic RSI
        - MACD, MACD.signal, MACD.histogram: MACD
        - ADX, ADX.plus_di, ADX.minus_di: ADX
        - CCI: Commodity Channel Index
    
    Returns:
        Dictionary with comprehensive metrics and signals, or None on error
    
    Example:
        >>> indicators = {
        ...     "open": 100.0, "close": 102.5,
        ...     "SMA20": 101.0, "BB.upper": 105.0, "BB.lower": 97.0,
        ...     "StochRSI.K": 35.0, "StochRSI.D": 30.0,
        ...     "MACD": 0.5, "MACD.signal": 0.3, "MACD.histogram": 0.2,
        ...     "ADX": 28.0, "ADX.plus_di": 25.0, "ADX.minus_di": 15.0,
        ...     "CCI": -50.0,
        ... }
        >>> result = compute_metrics(indicators)
    """
    # Use default weights if not provided
    weights = weights or DEFAULT_WEIGHTS
    
    try:
        # Validate input data
        if validate:
            validate_indicators(indicators)
        
        # Extract basic price data
        open_price = indicators["open"]
        close = indicators["close"]
        
        # Extract Bollinger Bands
        sma = indicators["SMA20"]
        bb_upper = indicators["BB.upper"]
        bb_lower = indicators["BB.lower"]
        bb_middle = sma
        
        # Extract Stochastic RSI
        stoch_k = indicators["StochRSI.K"]
        stoch_d = indicators["StochRSI.D"]
        
        # Extract MACD
        macd = indicators["MACD"]
        macd_signal_line = indicators["MACD.signal"]
        macd_histogram = indicators["MACD.histogram"]
        
        # Extract ADX
        adx = indicators["ADX"]
        plus_di = indicators["ADX.plus_di"]
        minus_di = indicators["ADX.minus_di"]
        
        # Extract CCI
        cci = indicators["CCI"]
        
        # Calculate basic metrics
        change = compute_change(open_price, close)
        bbw = compute_bbw(sma, bb_upper, bb_lower)
        
        # Calculate signals from each indicator
        bb_rating, bb_signal = compute_bb_rating_signal(close, bb_upper, bb_middle, bb_lower)
        stoch_rating, stoch_signal = compute_stoch_rsi_signal(stoch_k, stoch_d)
        macd_rating, macd_signal = compute_macd_signal(macd, macd_signal_line, macd_histogram)
        adx_rating, adx_signal, trend_strength = compute_adx_signal(adx, plus_di, minus_di)
        cci_rating, cci_signal = compute_cci_signal(cci)
        
        # Calculate composite signal
        ratings_list = [
            ("BB", bb_rating, weights.get("bb", 1.0)),
            ("StochRSI", stoch_rating, weights.get("stoch_rsi", 1.0)),
            ("MACD", macd_rating, weights.get("macd", 1.0)),
            ("ADX", adx_rating, weights.get("adx", 1.0)),
            ("CCI", cci_rating, weights.get("cci", 1.0)),
        ]
        
        composite_rating, composite_signal, breakdown = compute_composite_signal(ratings_list)
        
        # Build comprehensive result
        return {
            # Basic metrics
            "price": round(close, 4),
            "change": round(change, 3),
            
            # Composite signal (overall recommendation)
            "composite": {
                "rating": composite_rating,
                "signal": composite_signal,
                "breakdown": breakdown,
                "trend_strength": round(trend_strength, 2),
            },
            
            # Individual indicator signals
            "indicators": {
                "bollinger_bands": {
                    "rating": bb_rating,
                    "signal": bb_signal,
                    "width": round(bbw, 4) if bbw is not None else None,
                    "upper": round(bb_upper, 4),
                    "middle": round(bb_middle, 4),
                    "lower": round(bb_lower, 4),
                    "position": "above_upper" if close > bb_upper else "below_lower" if close < bb_lower else "in_range",
                },
                "stochastic_rsi": {
                    "rating": stoch_rating,
                    "signal": stoch_signal,
                    "k": round(stoch_k, 2),
                    "d": round(stoch_d, 2),
                    "position": "overbought" if stoch_k > 80 else "oversold" if stoch_k < 20 else "neutral",
                },
                "macd": {
                    "rating": macd_rating,
                    "signal": macd_signal,
                    "value": round(macd, 4),
                    "signal_line": round(macd_signal_line, 4),
                    "histogram": round(macd_histogram, 4),
                    "position": "above_signal" if macd > macd_signal_line else "below_signal",
                },
                "adx": {
                    "rating": adx_rating,
                    "signal": adx_signal,
                    "value": round(adx, 2),
                    "plus_di": round(plus_di, 2),
                    "minus_di": round(minus_di, 2),
                    "trend_strength": round(trend_strength, 2),
                    "trend_quality": "strong" if adx > 25 else "weak",
                },
                "cci": {
                    "rating": cci_rating,
                    "signal": cci_signal,
                    "value": round(cci, 2),
                    "position": "overbought" if cci > 100 else "oversold" if cci < -100 else "neutral",
                },
            },
        }
        
    except KeyError as e:
        logger.error(f"Missing required indicator: {e}", exc_info=True)
        return None
    except ValueError as e:
        logger.error(f"Invalid indicator values: {e}", exc_info=True)
        return None
    except (TypeError, ZeroDivisionError) as e:
        logger.error(f"Error computing metrics: {e}", exc_info=True)
        return None
