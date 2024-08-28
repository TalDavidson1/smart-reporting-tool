import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

class ExcelReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None

    def read_file(self) -> None:
        """Read the Excel file and store the data."""
        self.data = pd.read_excel(self.file_path)

    def get_data(self) -> pd.DataFrame:
        """Return the data as a pandas DataFrame."""
        if self.data is None:
            self.read_file()
        return self.data

    def get_total_sales_by_product(self, product: str) -> float:
        """Get total sales for a specific product."""
        if self.data is None:
            self.read_file()
        sales = self.data[self.data['Product'] == product]['Sales'].sum()
        print(f"DEBUG: Total sales for {product}: {sales}")
        return sales

    def get_total_sales_by_product_and_month(self, product: str, month: int) -> float:
        """Get total sales for a specific product in a given month."""
        if self.data is None:
            self.read_file()
        monthly_data = self.data[
            (self.data['Product'] == product) &
            (self.data['Date'].dt.month == month)
        ]
        sales = monthly_data['Sales'].sum()
        print(f"DEBUG: Total sales for {product} in month {month}: {sales}")
        return sales

# Create a mock dataset
def create_mock_dataset(file_path: str) -> None:
    """Create a mock Excel dataset with columns: Date, Product, Sales."""
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    num_days = len(date_range)

    products = ['Product A', 'Product B', 'Product C']
    sales = [100, 150, 200]

    data = {
        'Date': date_range,
        'Product': (products * (num_days // len(products) + 1))[:num_days],
        'Sales': (sales * (num_days // len(sales) + 1))[:num_days]
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

if __name__ == "__main__":
    # Create mock dataset
    mock_file_path = "mock_sales_data.xlsx"
    create_mock_dataset(mock_file_path)

    # Test ExcelReader
    reader = ExcelReader(mock_file_path)
    reader.read_file()
    print(reader.get_data().head())
    print(f"Total sales for Product A: {reader.get_total_sales_by_product('Product A')}")
    print(f"Total sales for Product A in January: {reader.get_total_sales_by_product_and_month('Product A', 1)}")
