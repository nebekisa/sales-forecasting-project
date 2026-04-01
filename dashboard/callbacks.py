"""
Interactive Callbacks Module
Optimized callbacks with caching and performance improvements
"""

import pandas as pd
import json
from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
import logging

from dashboard.data_loader import data_loader
from dashboard.charts import (
    create_advanced_forecast_chart,
    create_actual_vs_forecast_chart,
    create_store_radar_chart,
    create_model_performance_panel,
    create_anomaly_detection_chart
)

logger = logging.getLogger(__name__)

def register_callbacks(app):
    """Register all dashboard callbacks"""
    
    # Load data once at startup
    data = data_loader.get_data()
    historical_df = data.historical
    daily_forecast = data.daily_forecast
    store_forecast = data.store_forecast
    model_metadata = data.model_metadata
    
    @app.callback(
        Output('main-forecast', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date'),
         Input('store-selector', 'value'),
         Input('viz-mode', 'value')]
    )
    def update_forecast(start_date, end_date, store_selector, viz_mode):
        """Update forecast chart - optimized with pre-filtering"""
        if start_date and end_date:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            filtered_historical = historical_df[
                (historical_df['Date'] >= start) & 
                (historical_df['Date'] <= end)
            ]
        else:
            filtered_historical = historical_df.copy()
            start = filtered_historical['Date'].min()
            end = filtered_historical['Date'].max()
        
        # Create chart with selected mode
        fig = create_advanced_forecast_chart(
            filtered_historical, 
            daily_forecast, 
            store_selector, 
            viz_mode
        )
        
        # Add period highlight
        fig.add_vrect(
            x0=start, x1=end,
            fillcolor="yellow", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="Selected Period",
            annotation_position="top left"
        )
        
        return fig
    
    @app.callback(
        Output('actual-vs-forecast', 'figure'),
        [Input('store-selector', 'value')]
    )
    def update_actual_vs_forecast(store_selector):
        """Update actual vs forecast comparison"""
        return create_actual_vs_forecast_chart(
            historical_df, daily_forecast, store_selector
        )
    
    @app.callback(
        Output('store-radar', 'figure'),
        [Input('viz-mode', 'value')]
    )
    def update_store_radar(viz_mode):
        """Update store radar chart"""
        top_n = 5 if viz_mode == 'standard' else 10
        return create_store_radar_chart(store_forecast, top_n)
    
    @app.callback(
        Output('model-performance', 'figure'),
        [Input('viz-mode', 'value')]
    )
    def update_model_performance(viz_mode):
        """Update model performance panel"""
        return create_model_performance_panel(model_metadata)
    
    @app.callback(
        Output('anomaly-chart', 'figure'),
        [Input('date-range', 'start_date'),
         Input('date-range', 'end_date')]
    )
    def update_anomaly_chart(start_date, end_date):
        """Update anomaly detection chart"""
        if start_date and end_date:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            filtered_historical = historical_df[
                (historical_df['Date'] >= start) & 
                (historical_df['Date'] <= end)
            ]
        else:
            filtered_historical = historical_df
        
        return create_anomaly_detection_chart(filtered_historical)
    
    @app.callback(
        Output("download-csv", "data"),
        Input("export-csv-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_csv(n_clicks):
        """Export data as CSV"""
        if not n_clicks:
            raise PreventUpdate
        
        # Create export data
        export_data = daily_forecast.copy()
        export_data['Date'] = export_data['Date'].dt.strftime('%Y-%m-%d')
        
        return dict(content=export_data.to_csv(index=False), filename="sales_forecast.csv")