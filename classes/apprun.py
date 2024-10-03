import app
from collections import defaultdict
from classes.data_processor import DataProcessor
from collections import defaultdict
from classes.data_processor import DataProcessor

def apprun(dataConsumption, dataMeter):
    """
    Processes consumption and meter data for specified sensor IDs and runs the Dash app.

    Args:
        dataConsumption: The consumption data to process.
        dataMeter: The meter data to process.
    """
    # Initialize DataProcessor
    data_processor = DataProcessor()
    # List of IDs we are interested in
    sensor_ids = ["ID742", "ID735"]

    # Dictionaries to store data for each ID
    consumption_data_per_id = {}
    meter_data_per_id = {}

    def aggregate_entries(entries):
        """
        Aggregates entry data into time series, day totals, month totals, and year totals.

        Args:
            entries: A list of entries to aggregate.

        Returns:
            A dictionary containing aggregated data.
        """
        time_series_data = defaultdict(float)
        day_totals = defaultdict(float)
        month_totals = defaultdict(float)
        year_totals = defaultdict(float)

        for entry in entries:
            timestamp = entry.timestamp
            volume = entry.volume

            # Time series data (15-minute intervals)
            time_series_data[timestamp] += volume

            # Day totals
            date = timestamp.date()
            day_totals[date] += volume

            # Month totals
            year_month = (date.year, date.month)
            month_totals[year_month] += volume

            # Year totals
            year_totals[date.year] += volume

        return {
            'time_series_data': dict(time_series_data),
            'day_totals': dict(day_totals),
            'month_totals': dict(month_totals),
            'year_totals': dict(year_totals)
        }

    # Process consumption data
    for sensor_id in sensor_ids:
        sensor_data = data_processor.get_data(sensor_id, dataConsumption)

        # Check if data is available
        if not sensor_data:
            print(f"No data found for {sensor_id}.")
            continue

        # Collect all entries
        entries = [
            entry
            for consumption_data in sensor_data
            for entry in consumption_data.data
        ]

        # Aggregate data
        aggregated_data = aggregate_entries(entries)

        # Store the aggregated data for this ID
        consumption_data_per_id[sensor_id] = aggregated_data

    # Process meter data
    # Filter meter data to eliminate duplicates
    filtered_meter_data = data_processor.filter_meter_data(dataMeter)
    # Group meter data by month
    grouped_meter_data = data_processor.group_meter_data_by_month(
        filtered_meter_data
    )

    # Prepare data for each sensor ID
    for sensor_id in sensor_ids:
        dates = []
        totaltarif_values = []
        hochtarif_values = []
        niedertarif_values = []

        for meter_data_list in grouped_meter_data.values():
            for meter_data in meter_data_list:
                if sensor_id in meter_data.data:
                    dates.append(meter_data.timestamp)
                    reading = meter_data.get_reading(sensor_id)
                    totaltarif_values.append(reading.totalcost)
                    hochtarif_values.append(reading.highcost)
                    niedertarif_values.append(reading.lowcost)

        # Sort the dates and corresponding values
        sorted_data = sorted(
            zip(
                dates,
                totaltarif_values,
                hochtarif_values,
                niedertarif_values
            ),
            key=lambda x: x[0]
        )

        if sorted_data:
            (
                dates_sorted,
                totaltarif_values_sorted,
                hochtarif_values_sorted,
                niedertarif_values_sorted
            ) = zip(*sorted_data)
        else:
            dates_sorted = []
            totaltarif_values_sorted = []
            hochtarif_values_sorted = []
            niedertarif_values_sorted = []

        meter_data_per_id[sensor_id] = {
            'dates': dates_sorted,
            'totaltarif_values': totaltarif_values_sorted,
            'hochtarif_values': hochtarif_values_sorted,
            'niedertarif_values': niedertarif_values_sorted
        }

    # Start the Dash app, passing the data
    app.run_dash_app(consumption_data_per_id, meter_data_per_id)
