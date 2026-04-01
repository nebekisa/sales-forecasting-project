"""
UI Components Module
Reusable dashboard components with proper styling
"""

import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import timedelta
from typing import Optional, Dict, Any

from dashboard.config import COLORS, APP_CONFIG
from dashboard.data_loader import data_loader

def create_kpi_card(
    title: str,
    value: Any,
    subtitle: str,
    icon: str,
    color: str,
    trend: Optional[float] = None,
    trend_text: str = "vs last period"
) -> dbc.Card:
    """
    Professional KPI card with optional trend indicator
    """
    trend_icon = ""
    trend_color = ""
    if trend is not None:
        if trend > 0:
            trend_icon = "▲"
            trend_color = COLORS['success']
        elif trend < 0:
            trend_icon = "▼"
            trend_color = COLORS['danger']
    
    children = [
        html.Div([
            html.Div([
                html.I(className=f"fas fa-{icon} fa-2x", style={'color': color})
            ], className="float-end"),
            html.H6(title, className="text-muted mb-2", style={'fontSize': '14px'}),
            html.H2(str(value), className="mb-2", style={'fontWeight': '700'}),
            html.Small(subtitle, className="text-muted"),
            html.Br(),
        ])
    ]
    
    if trend is not None:
        children[0].children.append(
            html.Small(
                f"{trend_icon} {abs(trend)}% {trend_text}",
                style={'color': trend_color},
                className="mt-1 d-inline-block"
            )
        )
    
    return dbc.Card(
        dbc.CardBody(children),
        className="shadow-sm h-100",
        style={'borderTop': f'4px solid {color}', 'borderRadius': '10px'}
    )

def create_filter_panel() -> dbc.Card:
    """
    Create filter panel with date picker, store selector, and view mode
    """
    data = data_loader.get_data()
    historical_df = data.historical
    store_forecast = data.store_forecast
    
    return dbc.Card([
        dbc.CardBody([
            html.Label("📅 Analysis Period", className="fw-bold mb-2"),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=historical_df['Date'].min(),
                max_date_allowed=historical_df['Date'].max(),
                start_date=historical_df['Date'].max() - timedelta(days=APP_CONFIG.default_date_range_days),
                end_date=historical_df['Date'].max(),
                display_format='DD/MM/YYYY',
                className="mb-3",
                style={'width': '100%'}
            ),
            
            html.Label("🏪 Store Selection", className="fw-bold mb-2"),
            dcc.Dropdown(
                id='store-selector',
                options=[{'label': 'All Stores', 'value': 'all'}] + 
                        [{'label': f'Store {int(s)}', 'value': str(s)} 
                         for s in sorted(store_forecast['Store'].head(20))],
                value='all',
                placeholder="Select store to analyze",
                className="mb-3"
            ),
            
            html.Label("📊 Visualization Mode", className="fw-bold mb-2"),
            dcc.RadioItems(
                id='viz-mode',
                options=[
                    {'label': ' Standard View', 'value': 'standard'},
                    {'label': ' Detailed Analysis', 'value': 'detailed'},
                    {'label': ' Executive Summary', 'value': 'executive'}
                ],
                value='standard',
                inline=True,
                className="mb-2"
            ),
            
            html.Hr(),
            
            html.Label("📤 Export Options", className="fw-bold mb-2"),
            html.Div([
                dbc.Button("Export CSV", id="export-csv-btn", color="primary", size="sm", className="me-2"),
                dbc.Button("Export Chart", id="export-chart-btn", color="secondary", size="sm"),
            ]),
            
            dcc.Download(id="download-csv"),
        ])
    ], className="shadow-sm")