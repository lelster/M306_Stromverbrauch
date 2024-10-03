"""# app.py"""
import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


# Define global variables to store data
consumption_data_per_id = {}
meter_data_per_id = {}

def run_dash_app(consumption_data_arg, meter_data_arg, costtypevalue):
    global consumption_data_per_id, meter_data_per_id
    consumption_data_per_id = consumption_data_arg
    meter_data_per_id = meter_data_arg

    # Create the Dash app
    app = dash.Dash(__name__)

    # List of sensor IDs
    sensor_ids = list(consumption_data_per_id.keys())
    cost_types = ["Totaltarif", "Hochtarif", "Niedertrarif"]

    # Set initial sensor ID
    initial_sensor_id = sensor_ids[0]
    initial_cost_type = "Totaltarif"

    # Chart types
    chart_types = ['Line Chart', 'Bar Chart']
    initial_chart_type = 'Line Chart'

    # Prepare initial data for the initial sensor ID and chart type
    def prepare_initial_data(sensor_id, chart_type):
        if chart_type == 'Line Chart':
            sensor_data = consumption_data_per_id[sensor_id]
            year_totals = sensor_data['year_totals']
            years = sorted(year_totals.keys())
            year_values = [year_totals[year] for year in years]
            x_years = [datetime.datetime(year, 1, 1) for year in years]
            return x_years, year_values
        elif chart_type == 'Bar Chart':
            dates = meter_data_per_id[sensor_id]['dates']
            values = meter_data_per_id[sensor_id]['values']
            return dates, values

    x_data, y_data = prepare_initial_data(initial_sensor_id, initial_chart_type)

    # Initial figure
    if initial_chart_type == 'Line Chart':
        fig = go.Figure(
            data=[go.Scatter(x=x_data, y=y_data, mode='lines+markers')],
            layout=go.Layout(
                title=f'Yearly Consumption for {initial_sensor_id}',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Consumption (kWh)'},
            )
        )
    else:
        fig = go.Figure(
            data=[go.Bar(x=x_data, y=y_data)],
            layout=go.Layout(
                title=f'Meter Data for {initial_sensor_id}',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Value (kWh)'},
                barmode='group'
            )
        )

    app.layout = html.Div([
        html.Div([
            html.Label('Wähle Chart Type:'),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[{'label': ct, 'value': ct} for ct in chart_types],
                value=initial_chart_type,
                searchable=False,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Wähle Sensor ID:'),
            dcc.Dropdown(
                id='sensor-id-dropdown',
                options=[{'label': id_, 'value': id_} for id_ in sensor_ids],
                value=initial_sensor_id,
                searchable=False,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '10px'}),
                html.Div([
            html.Label('Tarif Typ wählen:'),
            dcc.Dropdown(
                id='cost-type-dropdown',
                options=[{'label': id_, 'value': id_} for id_ in cost_types],
                value=initial_cost_type,
                searchable=False,
                clearable=False
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'marginLeft': '10px'}),
        dcc.Graph(
            id='main-graph',
            figure=fig,
            config={'scrollZoom': True}  # Enable scroll zooming
        ),
    ])

    @app.callback(
        Output('main-graph', 'figure'),
        Input('chart-type-dropdown', 'value'),
        Input('sensor-id-dropdown', 'value'),
        Input('cost-type-dropdown', 'value'),
        Input('main-graph', 'relayoutData'),
        State('main-graph', 'figure')
    )
    def update_graph(selected_chart_type, selected_sensor_id, costtypeval, relayoutData, current_fig):
        # Prepare data based on chart type
        costtypevalue(costtypeval)
        if selected_chart_type == 'Line Chart':
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
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Consumption (kWh)'},
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
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Consumption (kWh)'},
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
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Consumption (kWh)'},
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
                        xaxis={'title': 'Month'},
                        yaxis={'title': 'Consumption (kWh)'},
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
                        xaxis={'title': 'Day'},
                        yaxis={'title': 'Consumption (kWh)'},
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
                        xaxis={'title': 'Time'},
                        yaxis={'title': 'Consumption (kWh)'},
                        xaxis_range=[x_min, x_max]
                    )
                )
                return new_fig
            else:
                return current_fig

        elif selected_chart_type == 'Bar Chart':
            dates = meter_data_per_id[selected_sensor_id]['dates']
            values = meter_data_per_id[selected_sensor_id]['values']

            # Create bar chart with rangeslider and buttons
            new_fig = go.Figure(
                data=[go.Bar(x=dates, y=values, name=f'Meter Data ({selected_sensor_id})')],
                layout=go.Layout(
                    title=f'Meter Data for {selected_sensor_id}',
                    xaxis={
                        'title': 'Date',
                        'type': 'date'
                    },
                    yaxis={'title': 'Value (kWh)'},
                    hovermode='closest',
                    barmode='group'
                )
            )
            return new_fig

    # Run the app
    app.run_server(debug=True)
