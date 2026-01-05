"""
Coinlist Module
--------------
Utilities for loading symbol lists from text files.
"""

import os
from typing import List

# Default coinlist directory (relative to project root)
COINLIST_DIR = os.path.join(os.path.dirname(__file__), "coinlist")


def load_symbols(exchange: str) -> List[str]:
    """
    Load symbols for a given exchange, with multiple fallback strategies.
    
    Args:
        exchange: Exchange name (e.g., 'BINANCE', 'KUCOIN')
        
    Returns:
        List of symbol strings (e.g., ['BINANCE:BTCUSDT', 'BINANCE:ETHUSDT'])
        Returns empty list if file not found or empty.
        
    Example:
        >>> symbols = load_symbols('BINANCE')
        >>> print(symbols[:3])
        ['BINANCE:BTCUSDT', 'BINANCE:ETHUSDT', 'BINANCE:SOLUSDT']
    """
    # Try multiple possible paths
    possible_paths = [
        os.path.join(COINLIST_DIR, f"{exchange}.txt"),
        os.path.join(COINLIST_DIR, f"{exchange.lower()}.txt"),
        # Fallback: relative to this file
        os.path.join(os.path.dirname(__file__), "coinlist", f"{exchange}.txt"),
        # Another fallback
        os.path.join(os.path.dirname(__file__), "coinlist", f"{exchange.lower()}.txt")
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                symbols = [line.strip() for line in content.split('\n') if line.strip()]
                if symbols:  # Only return if we actually got symbols
                    return symbols
        except (FileNotFoundError, IOError, UnicodeDecodeError):
            continue
    
    # If all fails, return empty list
    return []


def save_symbols(exchange: str, symbols: List[str]) -> bool:
    """
    Save symbols to a text file for the given exchange.
    
    Args:
        exchange: Exchange name (e.g., 'BINANCE')
        symbols: List of symbols to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure coinlist directory exists
        os.makedirs(COINLIST_DIR, exist_ok=True)
        
        filepath = os.path.join(COINLIST_DIR, f"{exchange}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(symbols))
        
        return True
    except (IOError, OSError) as e:
        print(f"Error saving symbols: {e}")
        return False


def list_available_exchanges() -> List[str]:
    """
    List all exchanges that have symbol files available.
    
    Returns:
        List of exchange names
    """
    if not os.path.exists(COINLIST_DIR):
        return []
    
    exchanges = []
    for filename in os.listdir(COINLIST_DIR):
        if filename.endswith('.txt'):
            exchange = filename[:-4].upper()  # Remove .txt and uppercase
            exchanges.append(exchange)
    
    return sorted(exchanges)
