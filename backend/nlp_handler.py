import spacy
from excel_reader import ExcelReader

class NLPHandler:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.excel_reader = ExcelReader("mock_sales_data.xlsx")
        self.excel_reader.read_file()

    def process_query(self, query: str):
        doc = self.nlp(query.lower())

        # Extract relevant information from the query
        product = None
        time_period = None

        for ent in doc.ents:
            if ent.label_ == "PRODUCT":
                product = ent.text
            elif ent.label_ == "DATE":
                time_period = ent.text

        # If no specific entities are found, look for keywords
        if not product:
            product = self._find_product(doc)
        if not time_period:
            time_period = self._find_time_period(doc)

        # Generate response based on extracted information
        if product and time_period:
            if time_period.lower() == "january":
                sales = self.excel_reader.get_total_sales_by_product_and_month(product, 1)
                return f"The total sales for {product} in {time_period} were ${sales:.2f}"
            else:
                sales = self.excel_reader.get_total_sales_by_product(product)
                return f"The total sales for {product} were ${sales:.2f}"
        elif product:
            sales = self.excel_reader.get_total_sales_by_product(product)
            return f"The total sales for {product} were ${sales:.2f}"
        else:
            return "I'm sorry, I couldn't understand your query. Please try asking about sales for a specific product or time period."

    def _find_product(self, doc):
        products = ["Product A", "Product B", "Product C"]
        for token in doc:
            if token.text in [p.lower() for p in products]:
                return token.text.capitalize()
        return None

    def _find_time_period(self, doc):
        months = ["january", "february", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november", "december"]
        for token in doc:
            if token.text in months:
                return token.text.capitalize()
        return None

# Example usage
if __name__ == "__main__":
    nlp_handler = NLPHandler()

    queries = [
        "What was the total sales for Product A in January?",
        "How much did Product B sell?",
        "Show me the sales for Product C",
    ]

    for query in queries:
        print(f"Query: {query}")
        print(f"Response: {nlp_handler.process_query(query)}\n")
