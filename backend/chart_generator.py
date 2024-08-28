import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

class ChartGenerator:
    def __init__(self, data):
        self.data = data

    def generate_line_chart(self, product, time_period=None):
        # Filter data for specific product
        filtered_data = self.data[self.data['Product'] == product]

        if time_period:
            # If time_period is specified, filter for that year
            filtered_data = filtered_data[filtered_data['Date'].dt.year == int(time_period)]

        # Group by year and month, then sum sales
        monthly_sales = filtered_data.groupby(filtered_data['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
        monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()

        # Sort the data chronologically
        monthly_sales = monthly_sales.sort_values('Date')

        # Prepare data for frontend
        labels = monthly_sales['Date'].dt.strftime('%B %Y').tolist()
        data = monthly_sales['Sales'].tolist()

        return {
            'labels': labels,
            'data': data
        }

    def generate_pie_chart(self, time_period=None):
        if time_period:
            # Filter data for specific time period
            filtered_data = self.data[self.data['Date'].dt.year == int(time_period)]
        else:
            filtered_data = self.data

        # Group by product and sum sales
        product_sales = filtered_data.groupby('Product')['Sales'].sum().reset_index()

        # Prepare data for frontend
        labels = product_sales['Product'].tolist()
        data = product_sales['Sales'].tolist()

        return {
            'labels': labels,
            'data': data
        }

    def generate_sales_table(self, product, time_period=None):
        if time_period:
            # Filter data for specific product and time period
            filtered_data = self.data[(self.data['Product'] == product) & (self.data['Date'].dt.year == int(time_period))]
        else:
            # Filter data for specific product
            filtered_data = self.data[self.data['Product'] == product]

        # Group by month and sum sales
        monthly_sales = filtered_data.groupby(filtered_data['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
        monthly_sales['Month'] = monthly_sales['Date'].dt.strftime('%B')
        monthly_sales = monthly_sales[['Month', 'Sales']]

        # Add total row
        total_sales = monthly_sales['Sales'].sum()
        total_row = pd.DataFrame({'Month': ['Total'], 'Sales': [total_sales]})
        monthly_sales = pd.concat([monthly_sales, total_row], ignore_index=True)

        return monthly_sales.to_dict('records')

# Example usage
if __name__ == "__main__":
    # Create a sample dataset
    date_range = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')
    data = pd.DataFrame({
        'Date': date_range,
        'Product': ['Product A', 'Product B'] * (len(date_range) // 2),
        'Sales': [100, 150] * (len(date_range) // 2)
    })

    chart_generator = ChartGenerator(data)

    # Generate line chart
    line_chart = chart_generator.generate_line_chart('Product A', '2022')
    print("Line chart generated (base64 encoded):", line_chart[:50] + "...")

    # Generate sales table
    sales_table = chart_generator.generate_sales_table('Product A', '2022')
    print("Sales table generated:", sales_table)
