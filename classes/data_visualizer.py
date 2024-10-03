from plotly.graph_objs import Figure, Bar, Scatter

class DataVisualizer:
    """Class to generate Plotly charts for consumption and meter readings."""

    @staticmethod
    def generate_bar_chart(data: list, x_labels: list[str], title: str) -> Figure:
        """
        Generates a Plotly bar chart.

        :param data: The data to be visualized
        :param x_labels: Labels for the x-axis
        :param title: The chart title
        :return: A Plotly Figure object
        """
        chart = Bar(x=x_labels, y=data)

        fig = Figure(
            data=[chart],
            layout={
                'title': title,
                'xaxis': {'title': 'Time'},
                'yaxis': {'title': 'Consumption (Bar)'},
            }
        )
        return fig

    @staticmethod
    def generate_line_chart(data: list, x_labels: list[str], title: str) -> Figure:
        """
        Generates a Plotly line chart.

        :param data: The data to be visualized
        :param x_labels: Labels for the x-axis
        :param title: The chart title
        :return: A Plotly Figure object
        """
        chart = Scatter(x=x_labels, y=data, mode='lines+markers')

        fig = Figure(
            data=[chart],
            layout={
                'title': title,
                'xaxis': {'title': 'Time'},
                'yaxis': {'title': 'Consumption (Line)'},
            }
        )
        return fig
