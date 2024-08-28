import spacy
from spacy.matcher import Matcher
from excel_reader import ExcelReader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPHandler:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.excel_reader = ExcelReader("mock_sales_data.xlsx")
        self.excel_reader.read_file()
        self.matcher = Matcher(self.nlp.vocab)
        self._setup_custom_entities()

    def _setup_custom_entities(self):
        # Add custom patterns for products
        product_pattern = [
            {"LOWER": "product"},
            {"TEXT": {"REGEX": "^[A-D]$"}}
        ]
        self.matcher.add("PRODUCT", [product_pattern])

        # Add custom patterns for months
        month_pattern = [{"LOWER": {"IN": [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]}}]
        self.matcher.add("MONTH", [month_pattern])

    def process_query(self, query: str):
        try:
            logger.info(f"Processing query: {query}")
            doc = self.nlp(query)
            logger.info(f"Tokenized query: {[token.text for token in doc]}")

            product, time_period = self._extract_entities(doc)
            logger.info(f"Extracted entities - Product: {product}, Time Period: {time_period}")

            if product and time_period:
                month_num = self._month_to_number(time_period)
                logger.info(f"Converted time period to month number: {month_num}")
                if month_num:
                    sales = self.excel_reader.get_total_sales_by_product_and_month(product, month_num)
                    logger.info(f"Retrieved sales for {product} in {time_period}: ${sales:.2f}")
                    return f"The total sales for {product} in {time_period} were ${sales:.2f}"
                else:
                    sales = self.excel_reader.get_total_sales_by_product(product)
                    logger.info(f"Retrieved total sales for {product}: ${sales:.2f}")
                    return f"The total sales for {product} were ${sales:.2f}"
            elif product:
                sales = self.excel_reader.get_total_sales_by_product(product)
                logger.info(f"Retrieved total sales for {product}: ${sales:.2f}")
                return f"The total sales for {product} were ${sales:.2f}"
            else:
                logger.warning("Could not extract product or time period from query")
                return "I'm sorry, I couldn't understand your query. Please ask about sales for a specific product or time period."
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "An error occurred while processing your query. Please try again."

    def _extract_entities(self, doc):
        product = None
        time_period = None

        matches = self.matcher(doc)
        logger.info(f"Matcher found {len(matches)} matches")

        for match_id, start, end in matches:
            span = doc[start:end]
            if self.nlp.vocab.strings[match_id] == "PRODUCT":
                # Capture the full product name (e.g., "Product A")
                product = span.text
                logger.info(f"Recognized product: {product}")
            elif self.nlp.vocab.strings[match_id] == "MONTH":
                time_period = span.text.capitalize()
                logger.info(f"Recognized time period: {time_period}")

        return product, time_period

    def _month_to_number(self, month: str) -> int:
        months = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }
        return months.get(month.lower())

# Example usage
if __name__ == "__main__":
    nlp_handler = NLPHandler()

    queries = [
        "What was the total sales for Product A in January?",
        "How much did Product B sell?",
        "Show me the sales for Product C in March",
        "What about Product D in December?",
    ]

    for query in queries:
        print(f"Query: {query}")
        print(f"Response: {nlp_handler.process_query(query)}\n")
