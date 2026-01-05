"""
Binance API Integration Module
------------------------------
Direct integration with Binance API for trading operations.
Works independently of MCP servers.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from decimal import Decimal

logger = logging.getLogger(__name__)

# Try to import binance library
try:
    from binance.client import Client
    from binance.exceptions import BinanceAPIException
    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False
    logger.warning("python-binance not installed. Install with: pip install python-binance")


class BinanceIntegration:
    """
    Binance API integration for trading operations.
    
    Usage:
        >>> binance = BinanceIntegration()
        >>> balance = binance.get_account_balance()
        >>> price = binance.get_current_price("BTCUSDT")
    """
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key (defaults to env var BINANCE_API_KEY)
            api_secret: Binance API secret (defaults to env var BINANCE_API_SECRET)
        """
        if not BINANCE_AVAILABLE:
            raise ImportError("python-binance not installed. Run: pip install python-binance")
        
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            logger.warning("Binance API credentials not provided. Some functions will not work.")
            self.client = None
        else:
            self.client = Client(self.api_key, self.api_secret)
    
    def get_account_balance(self) -> Dict[str, float]:
        """
        Get account balances for all assets.
        
        Returns:
            Dictionary of {asset: balance} for non-zero balances
        """
        if not self.client:
            raise ValueError("Binance client not initialized. Provide API credentials.")
        
        try:
            account = self.client.get_account()
            balances = {}
            
            for balance in account['balances']:
                asset = balance['asset']
                free = float(balance['free'])
                locked = float(balance['locked'])
                total = free + locked
                
                if total > 0:
                    balances[asset] = {
                        'free': free,
                        'locked': locked,
                        'total': total
                    }
            
            return balances
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            return {}
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            
        Returns:
            Current price or None if error
        """
        if not self.client:
            # Can get price without authentication
            self.client = Client("", "")
        
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_24h_stats(self, symbol: str) -> Optional[Dict]:
        """
        Get 24-hour statistics for a symbol.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            
        Returns:
            Dictionary with 24h stats or None if error
        """
        if not self.client:
            self.client = Client("", "")
        
        try:
            stats = self.client.get_ticker(symbol=symbol)
            return {
                'symbol': stats['symbol'],
                'price': float(stats['lastPrice']),
                'price_change': float(stats['priceChange']),
                'price_change_percent': float(stats['priceChangePercent']),
                'high': float(stats['highPrice']),
                'low': float(stats['lowPrice']),
                'volume': float(stats['volume']),
                'quote_volume': float(stats['quoteVolume']),
            }
        except BinanceAPIException as e:
            logger.error(f"Error fetching stats for {symbol}: {e}")
            return None
    
    def get_order_book(self, symbol: str, limit: int = 10) -> Optional[Dict]:
        """
        Get order book for a symbol.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            limit: Number of levels to fetch (default: 10)
            
        Returns:
            Dictionary with bids and asks or None if error
        """
        if not self.client:
            self.client = Client("", "")
        
        try:
            depth = self.client.get_order_book(symbol=symbol, limit=limit)
            return {
                'bids': [[float(price), float(qty)] for price, qty in depth['bids']],
                'asks': [[float(price), float(qty)] for price, qty in depth['asks']],
            }
        except BinanceAPIException as e:
            logger.error(f"Error fetching order book for {symbol}: {e}")
            return None
    
    def place_test_order(self, symbol: str, side: str, quantity: float, order_type: str = "MARKET") -> bool:
        """
        Place a test order (does not execute).
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            order_type: 'MARKET' or 'LIMIT'
            
        Returns:
            True if test successful, False otherwise
        """
        if not self.client:
            raise ValueError("Binance client not initialized. Provide API credentials.")
        
        try:
            if order_type == "MARKET":
                self.client.create_test_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            else:
                logger.warning("LIMIT orders require price parameter")
                return False
            
            logger.info(f"Test order successful: {side} {quantity} {symbol}")
            return True
        except BinanceAPIException as e:
            logger.error(f"Test order failed: {e}")
            return False


def normalize_symbol(symbol: str) -> str:
    """
    Normalize symbol from TradingView format to Binance format.
    
    Args:
        symbol: Symbol in format 'BINANCE:BTCUSDT' or 'BTCUSDT'
        
    Returns:
        Symbol in Binance format 'BTCUSDT'
    """
    if ':' in symbol:
        return symbol.split(':')[1]
    return symbol


def get_binance_prices(symbols: List[str]) -> Dict[str, float]:
    """
    Get current prices for multiple symbols.
    
    Args:
        symbols: List of symbols (can be in TradingView or Binance format)
        
    Returns:
        Dictionary of {symbol: price}
    """
    binance = BinanceIntegration()
    prices = {}
    
    for symbol in symbols:
        normalized = normalize_symbol(symbol)
        price = binance.get_current_price(normalized)
        if price:
            prices[symbol] = price
    
    return prices
