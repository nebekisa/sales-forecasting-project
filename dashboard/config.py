"""
Enterprise Dashboard Configuration
Author: Senior Data Scientist
Version: 3.0.0
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"

# ============================================================================
# COLOR SCHEME (Enterprise Branding)
# ============================================================================

COLORS: Dict[str, str] = {
    'primary': '#2C3E50',      # Dark blue-gray
    'secondary': '#E74C3C',     # Coral red
    'success': '#27AE60',       # Green
    'info': '#3498DB',          # Light blue
    'warning': '#F39C12',       # Orange
    'danger': '#E74C3C',        # Red
    'dark': '#1A2632',          # Almost black
    'light': '#ECF0F1',         # Light gray
    'white': '#FFFFFF',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# ============================================================================
# APP CONFIGURATION
# ============================================================================

@dataclass
class AppConfig:
    """Application configuration"""
    title: str = "ROSSMANN Sales Intelligence Platform"
    version: str = "3.0.0"
    edition: str = "Enterprise"
    debug: bool = True
    port: int = 8050
    host: str = "127.0.0.1"
    
    # Dashboard settings
    default_date_range_days: int = 90
    confidence_level: float = 0.95
    top_stores_count: int = 50
    
    # Performance settings
    enable_caching: bool = True
    cache_timeout: int = 300  # seconds

APP_CONFIG = AppConfig()

# ============================================================================
# THEME
# ============================================================================

EXTERNAL_STYLESHEETS = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
]