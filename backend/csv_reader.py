import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.column_mapping = {}

    def read_file(self) -> None:
        """Read the CSV file and store the data with dynamic column handling."""
        try:
            self.data = pd.read_csv(self.file_path)
            self._infer_column_types()
            self._map_columns()
            logger.info(f"Successfully read CSV file: {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise

    def _infer_column_types(self):
        """Infer and convert column types."""
        for column in self.data.columns:
            if 'date' in column.lower():
                self.data[column] = pd.to_datetime(self.data[column], errors='coerce')
            elif 'sales' in column.lower() or 'revenue' in column.lower():
                self.data[column] = pd.to_numeric(self.data[column], errors='coerce')

    def _map_columns(self):
        """Map columns to standard names."""
        for column in self.data.columns:
            if 'date' in column.lower():
                self.column_mapping['date'] = column
            elif 'product' in column.lower():
                self.column_mapping['product'] = column
            elif 'sales' in column.lower() or 'revenue' in column.lower():
                self.column_mapping['sales'] = column

    def get_data(self) -> pd.DataFrame:
        """Return the data as a pandas DataFrame."""
        if self.data is None:
            self.read_file()
        return self.data

    def get_total_sales_by_product(self, product: str) -> float:
        """Get total sales for a specific product."""
        if self.data is None:
            self.read_file()
        try:
            sales = self.data[self.data[self.column_mapping['product']] == product][self.column_mapping['sales']].sum()
            logger.info(f"Total sales for {product}: {sales}")
            return sales
        except KeyError as e:
            logger.error(f"Column not found: {str(e)}")
            raise ValueError(f"Required column not found in the CSV file: {str(e)}")

    def get_total_sales_by_product_and_month(self, product: str, month: int) -> float:
        """Get total sales for a specific product in a given month."""
        if self.data is None:
            self.read_file()
        try:
            monthly_data = self.data[
                (self.data[self.column_mapping['product']] == product) &
                (self.data[self.column_mapping['date']].dt.month == month)
            ]
            sales = monthly_data[self.column_mapping['sales']].sum()
            logger.info(f"Total sales for {product} in month {month}: {sales}")
            return sales
        except KeyError as e:
            logger.error(f"Column not found: {str(e)}")
            raise ValueError(f"Required column not found in the CSV file: {str(e)}")

    def get_sales_data_by_product(self, product: str) -> List[Dict[str, Any]]:
        """Get sales data for a specific product."""
        if self.data is None:
            self.read_file()
        try:
            product_data = self.data[self.data[self.column_mapping['product']] == product]
            return product_data.to_dict('records')
        except KeyError as e:
            logger.error(f"Column not found: {str(e)}")
            raise ValueError(f"Required column not found in the CSV file: {str(e)}")

    def get_sales_data_by_product_and_month(self, product: str, month: int) -> List[Dict[str, Any]]:
        """Get sales data for a specific product and month."""
        if self.data is None:
            self.read_file()
        try:
            product_month_data = self.data[
                (self.data[self.column_mapping['product']] == product) &
                (self.data[self.column_mapping['date']].dt.month == month)
            ]
            return product_month_data.to_dict('records')
        except KeyError as e:
            logger.error(f"Column not found: {str(e)}")
            raise ValueError(f"Required column not found in the CSV file: {str(e)}")

# Create a mock dataset
def create_mock_dataset(file_path: str) -> None:
    """Create a mock CSV dataset with columns: Date, Product, Sales."""
    date_range = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    num_days = len(date_range)

    products = ['Product A', 'Product B', 'Product C']
    np.random.seed(42)  # For reproducibility
    sales = np.random.randint(500, 3000, size=num_days * len(products))

    data = {
        'Date': date_range.repeat(3),
        'Product': products * num_days,
        'Sales': sales
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    # Create mock dataset
    mock_file_path = "mock_sales_data.csv"
    create_mock_dataset(mock_file_path)

    # Test CSVReader
    reader = CSVReader(mock_file_path)
    reader.read_file()
    print(reader.get_data().head())
    print(f"Total sales for Product A: {reader.get_total_sales_by_product('Product A')}")
    print(f"Total sales for Product A in January: {reader.get_total_sales_by_product_and_month('Product A', 1)}")
