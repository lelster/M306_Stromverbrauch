import os
import webbrowser
from classes.data_processor import DataProcessor
import app


def apprun(dataConsumption, dataMeter):
    data_processor = DataProcessor()
    sensor_ids = ["ID742", "ID735"]

    # Dictionary to store data for each ID
    consumption_data_per_id = {}
    meter_data_per_id = {}

    # Variable to track the cost type
    cost_type_value = "Totaltarif"

    def cost_type_callback(value: str):
        nonlocal cost_type_value  # Use nonlocal to modify the enclosing scope variable
        cost_type_value = value
        print(f"Cost type updated: {cost_type_value}")

    # Process consumption data
    for sensor_id in sensor_ids:
        sensor_data = data_processor.get_data(sensor_id, dataConsumption)

        # Check if data is available
        if not sensor_data:
            print(f"No data found for {sensor_id}.")
            continue

        # Collect all entries
        entries = []
        for consumption_data in sensor_data:
            entries.extend(consumption_data.data)

        # Aggregate data
        # Time series data (15-minute intervals)
        time_series_data = {}
        for entry in entries:
            timestamp = entry.timestamp
            time_series_data[timestamp] = time_series_data.get(timestamp, 0) + entry.volume

        # Day totals
        day_totals = {}
        for timestamp, volume in time_series_data.items():
            date = timestamp.date()
            day_totals[date] = day_totals.get(date, 0) + volume

        # Month totals
        month_totals = {}
        for date, total in day_totals.items():
            year_month = (date.year, date.month)
            month_totals[year_month] = month_totals.get(year_month, 0) + total

        # Year totals
        year_totals = {}
        for (year, month), total in month_totals.items():
            year_totals[year] = year_totals.get(year, 0) + total

        # Store the aggregated data for this ID
        consumption_data_per_id[sensor_id] = {
            'time_series_data': time_series_data,
            'day_totals': day_totals,
            'month_totals': month_totals,
            'year_totals': year_totals
        }

    # Process meter data
    # Filter meter data to eliminate duplicates
    filtered_meter_data = data_processor.filter_meter_data(dataMeter)
    # Group meter data by month
    grouped_meter_data = data_processor.group_meter_data_by_month(filtered_meter_data)

    # Prepare data for each sensor ID
    for sensor_id in sensor_ids:
        dates = []
        values = []
        for (year, month), meter_data_list in grouped_meter_data.items():
            for meter_data in meter_data_list:
                if sensor_id in meter_data.data:
                    reading = meter_data.get_reading(sensor_id)
                    # Determine the correct value based on the cost type
                    value = (
                        reading.totalcost if cost_type_value == "Totaltarif" else
                        reading.highcost if cost_type_value == "Hochtarif" else
                        reading.lowcost
                    )
                    dates.append(meter_data.timestamp)
                    values.append(value)

        # Sort the dates and values
        sorted_pairs = sorted(zip(dates, values), key=lambda x: x[0])
        dates_sorted, values_sorted = zip(*sorted_pairs) if sorted_pairs else ([], [])
        meter_data_per_id[sensor_id] = {
            'dates': dates_sorted,
            'values': values_sorted
        }

    # Only open the browser if data for both sensors is processed correctly
    if consumption_data_per_id and meter_data_per_id:
        def open_browser():
            if not os.environ.get("WERKZEUG_RUN_MAIN"):  # Only open the browser if it's the main thread
                webbrowser.open_new('http://127.0.0.1:8050/')

        # Run the Dash app and open the browser after ensuring data is ready
        app.run_dash_app(consumption_data_per_id, meter_data_per_id, cost_type_callback)
        open_browser()
    else:
        print("Data processing failed or no data available. The browser will not be opened.")
