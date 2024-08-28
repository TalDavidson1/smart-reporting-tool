import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

class ChartGenerator:
    def __init__(self, data):
        self.data = data

    def generate_line_chart(self, product, time_period=None):
        if time_period:
            # Filter data for specific product and time period
            filtered_data = self.data[(self.data['Product'] == product) & (self.data['Date'].dt.year == int(time_period))]
        else:
            # Filter data for specific product
            filtered_data = self.data[self.data['Product'] == product]

        # Group by month and sum sales
        monthly_sales = filtered_data.groupby(filtered_data['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
        monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()

        # Create line chart
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_sales['Date'], monthly_sales['Sales'])
        plt.title(f'Sales Trend for {product}')
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.grid(True)

        # Save plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Encode the image to base64
        encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')

        plt.close()

        return encoded_img

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
        monthly_sales = monthly_sales.append({'Month': 'Total', 'Sales': total_sales}, ignore_index=True)

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
