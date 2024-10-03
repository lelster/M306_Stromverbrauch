# app.py

import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# Define global variables to store data
consumption_data_per_id = {}
meter_data_per_id = {}

def run_dash_app(consumption_data_arg, meter_data_arg):
    global consumption_data_per_id, meter_data_per_id
    consumption_data_per_id = consumption_data_arg
    meter_data_per_id = meter_data_arg

    # Create the Dash app
    app = dash.Dash(__name__)

    # List of sensor IDs
    sensor_ids = list(consumption_data_per_id.keys())

    # Set initial sensor ID
    initial_sensor_id = sensor_ids[0]

    # Chart types
    chart_types = ['Liniendiagramm', 'Balkendiagramm']
    initial_chart_type = 'Liniendiagramm'

    # Prepare initial data for the initial sensor ID and chart type
    def prepare_initial_data(sensor_id, chart_type):
        if chart_type == 'Liniendiagramm':
            sensor_data = consumption_data_per_id[sensor_id]
            year_totals = sensor_data['year_totals']
            years = sorted(year_totals.keys())
            year_values = [year_totals[year] for year in years]
            x_years = [datetime.datetime(year, 1, 1) for year in years]
            return x_years, year_values
        elif chart_type == 'Balkendiagramm':
            dates = meter_data_per_id[sensor_id]['dates']
            totaltarif_values = meter_data_per_id[sensor_id]['totaltarif_values']
            hochtarif_values = meter_data_per_id[sensor_id]['hochtarif_values']
            niedertarif_values = meter_data_per_id[sensor_id]['niedertarif_values']
            return dates, totaltarif_values, hochtarif_values, niedertarif_values

    # Prepare initial data
    x_data, y_data = prepare_initial_data(initial_sensor_id, initial_chart_type)

    # Initial figure
    if initial_chart_type == 'Liniendiagramm':
        fig = go.Figure(
            data=[go.Scatter(x=x_data, y=y_data, mode='lines+markers')],
            layout=go.Layout(
                title=f'Jährlicher Konsum für {initial_sensor_id}',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Konsum (kWh)'},
            )
        )
    else:
        dates, totaltarif_values, hochtarif_values, niedertarif_values = prepare_initial_data(initial_sensor_id, initial_chart_type)
        # Since initial stacked view is off, show Totaltarif
        fig = go.Figure(
            data=[go.Bar(x=dates, y=totaltarif_values, name='Totaltarif')],
            layout=go.Layout(
                title=f'Meter Daten für {initial_sensor_id} (Totaltarif)',
                xaxis={'title': 'Datum'},
                yaxis={'title': 'Wert (kWh)'},
                barmode='group'
            )
        )

    app.layout = html.Div([
        html.Div([
            html.Label('Wähle Diagrammart:'),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[{'label': ct, 'value': ct} for ct in chart_types],
                value=initial_chart_type,
                searchable=False,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Sensor ID auswählen:'),
            dcc.Dropdown(
                id='sensor-id-dropdown',
                options=[{'label': id_, 'value': id_} for id_ in sensor_ids],
                value=initial_sensor_id,
                searchable=False,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '10px'}),
        html.Div([
            html.Label('Gestapelte Ansicht:'),
            dcc.Checklist(
                id='stacked-view-checkbox',
                options=[{'label': 'Aktivieren', 'value': 'stacked'}],
                value=[],
                labelStyle={'display': 'inline-block'}
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '10px', 'marginTop': '100px'}, id='stacked-view-checkbox-div'),
        dcc.Graph(
            id='main-graph',
            figure=fig,
            config={'scrollZoom': True}  # Aktivieren scroll zooming
        ),
    ])

    @app.callback(
        Output('main-graph', 'figure'),
        Input('chart-type-dropdown', 'value'),
        Input('sensor-id-dropdown', 'value'),
        Input('stacked-view-checkbox', 'value'),
        Input('main-graph', 'relayoutData'),
        State('main-graph', 'figure')
    )
    def update_graph(selected_chart_type, selected_sensor_id, stacked_view, relayoutData, current_fig):
        # Prepare data based on chart type
        if selected_chart_type == 'Liniendiagramm':
            sensor_data = consumption_data_per_id[selected_sensor_id]
            time_series_data = sensor_data['time_series_data']
            day_totals = sensor_data['day_totals']
            month_totals = sensor_data['month_totals']
            year_totals = sensor_data['year_totals']

            years = sorted(year_totals.keys())
            x_years = [datetime.datetime(year, 1, 1) for year in years]
            year_values = [year_totals[year] for year in years]

            # If relayoutData is None or doesn't have 'xaxis.range[0]', return the initial figure
            if relayoutData is None or 'xaxis.range[0]' not in relayoutData:
                new_fig = go.Figure(
                    data=[go.Scatter(x=x_years, y=year_values, mode='lines+markers')],
                    layout=go.Layout(
                        title=f'Jährliche Statistik für {selected_sensor_id}',
                        xaxis={'title': 'Jahr'},
                        yaxis={'title': 'Konsum (kWh)'},
                    )
                )
                return new_fig

            # Get the current x-axis range
            x_min_str = relayoutData.get('xaxis.range[0]', None)
            x_max_str = relayoutData.get('xaxis.range[1]', None)
            if x_min_str is None or x_max_str is None:
                new_fig = go.Figure(
                    data=[go.Scatter(x=x_years, y=year_values, mode='lines+markers')],
                    layout=go.Layout(
                        title=f'Jährliche Statistik für {selected_sensor_id}',
                        xaxis={'title': 'Jahr'},
                        yaxis={'title': 'Konsum (kWh)'},
                    )
                )
                return new_fig

            x_min = datetime.datetime.fromisoformat(x_min_str)
            x_max = datetime.datetime.fromisoformat(x_max_str)

            # Calculate range in days
            range_days = (x_max - x_min).days

            if range_days > 730:
                # Show yearly data
                new_fig = go.Figure(
                    data=[go.Scatter(x=x_years, y=year_values, mode='lines+markers')],
                    layout=go.Layout(
                        title=f'Jährliche Statistik für {selected_sensor_id}',
                        xaxis={'title': 'Jahr'},
                        yaxis={'title': 'Konsum (kWh)'},
                        xaxis_range=[x_min, x_max]
                    )
                )
                return new_fig
            elif 60 < range_days <= 730:
                # Show monthly data
                months = sorted(month_totals.keys())
                x_months = [datetime.datetime(year, month, 1) for year, month in months]
                month_values = [month_totals[(year, month)] for year, month in months]

                # Filter months within the x-axis range
                x_months_filtered = []
                month_values_filtered = []
                for x, y in zip(x_months, month_values):
                    if x_min <= x <= x_max:
                        x_months_filtered.append(x)
                        month_values_filtered.append(y)
                new_fig = go.Figure(
                    data=[go.Scatter(x=x_months_filtered, y=month_values_filtered, mode='lines+markers')],
                    layout=go.Layout(
                        title=f'Monatliche Statistik für {selected_sensor_id}',
                        xaxis={'title': 'Monat'},
                        yaxis={'title': 'Konsum (kWh)'},
                        xaxis_range=[x_min, x_max]
                    )
                )
                return new_fig
            elif 2 < range_days <= 60:
                # Show daily data
                days = sorted(day_totals.keys())
                x_days = [datetime.datetime.combine(date, datetime.time()) for date in days]
                day_values = [day_totals[date] for date in days]

                # Filter days within the x-axis range
                x_days_filtered = []
                day_values_filtered = []
                for x, y in zip(x_days, day_values):
                    if x_min <= x <= x_max:
                        x_days_filtered.append(x)
                        day_values_filtered.append(y)

                new_fig = go.Figure(
                    data=[go.Scatter(x=x_days_filtered, y=day_values_filtered, mode='lines+markers')],
                    layout=go.Layout(
                        title=f'Tägliche Statistik für {selected_sensor_id}',
                        xaxis={'title': 'Tag'},
                        yaxis={'title': 'Konsum (kWh)'},
                        xaxis_range=[x_min, x_max]
                    )
                )
                return new_fig
            elif range_days <= 2:
                # Show 15-minute data
                timestamps = sorted(time_series_data.keys())
                x_times = [ts for ts in timestamps if x_min <= ts <= x_max]
                y_values = [time_series_data[ts] for ts in x_times]

                new_fig = go.Figure(
                    data=[go.Scatter(x=x_times, y=y_values, mode='lines+markers')],
                    layout=go.Layout(
                        title=f'15-Minuten Statistik für {selected_sensor_id}',
                        xaxis={'title': 'Zeit'},
                        yaxis={'title': 'Konsum (kWh)'},
                        xaxis_range=[x_min, x_max]
                    )
                )
                return new_fig
            else:
                return current_fig

            # Handle zooming and panning here (omitted for brevity)

        elif selected_chart_type == 'Balkendiagramm':
            dates = meter_data_per_id[selected_sensor_id]['dates']
            totaltarif_values = meter_data_per_id[selected_sensor_id]['totaltarif_values']
            hochtarif_values = meter_data_per_id[selected_sensor_id]['hochtarif_values']
            niedertarif_values = meter_data_per_id[selected_sensor_id]['niedertarif_values']

            if 'stacked' in stacked_view:
                data_traces = [
                    go.Bar(x=dates, y=hochtarif_values, name='Hochtarif'),
                    go.Bar(x=dates, y=niedertarif_values, name='Niedertarif')
                ]
                barmode = 'stack'
                title = f'Meter Daten für {selected_sensor_id} (Gestapelt Hochtarif and Niedertarif)'
            else:
                data_traces = [go.Bar(x=dates, y=totaltarif_values, name='Totaltarif')]
                barmode = 'group'
                title = f'Meter Daten für {selected_sensor_id} (Totaltarif)'

            # Create bar chart
            new_fig = go.Figure(
                data=data_traces,
                layout=go.Layout(
                    title=title,
                    xaxis={
                        'title': 'Datum',
                        'type': 'date'
                    },
                    yaxis={'title': 'Wert (kWh)'},
                    hovermode='closest',
                    barmode=barmode
                )
            )
            return new_fig

    @app.callback(
        Output('stacked-view-checkbox-div', 'style'),
        Input('chart-type-dropdown', 'value'),
    )
    def toggle_stacked_view_visibility(selected_chart_type):
        if selected_chart_type == 'Balkendiagramm':
            return {'width': '20%', 'display': 'inline-block', 'marginLeft': '10px'}
        else:
            return {'display': 'none'}

    app.run_server(debug=True)