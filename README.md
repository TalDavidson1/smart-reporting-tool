# Smart Reporting Tool

## Project Description

The Smart Reporting Tool is an advanced reporting software that connects to various data sources and uses Natural Language Processing (NLP) to interpret user questions and generate visualizations. This tool allows Database Administrators (DBAs) to connect data sources to the backend, while end-users can ask questions using natural language to generate visual reports.

### Key Features:
- Connects to various data sources (currently Excel files, with plans to expand to SQL databases)
- Uses NLP to interpret user queries and generate relevant visualizations
- Backend built with FastAPI for efficient API development
- Frontend developed using React with Chakra UI for a responsive interface
- Initial focus on Excel files with columns: Date, Product, Sales
- Sample query: "What was the total sales for Product A in January?"

### Current Progress:
- Backend API implemented with FastAPI
- Frontend skeleton developed using React and Chakra UI
- NLP query handling implemented for basic sales queries
- Excel file reader with mock dataset created

### Challenges:
- React rendering issues and module import problems (currently being addressed)

### Future Expansion Plans:
- Connect to various SQL databases (MSSQL, MySQL, PostgreSQL, Oracle, Azure)
- Implement more advanced visualization options
- Design system for scalability to accommodate multiple data sources

## Project Structure

```
smart-reporting-tool/
├── backend/
│   ├── main.py
│   ├── excel_reader.py
│   ├── nlp_handler.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── ColorModeSwitcher.js
│   │   └── index.js
│   └── package.json
├── .gitignore
├── README.md
└── test-embed.html
```

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/your-username/smart-reporting-tool.git
   cd smart-reporting-tool
   ```

2. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   uvicorn main:app --reload
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000` to use the tool.

## Embedding the Smart Reporting Tool

To embed the Smart Reporting Tool into your website, follow these steps:

1. Include the necessary script in your HTML file:
   ```html
   <script src="path/to/main.0a7877dd.js"></script>
   ```

2. Add a container element where you want the tool to appear:
   ```html
   <div id="smart-reporting-tool-container"></div>
   ```

3. Initialize the Smart Reporting Tool with configuration options:
   ```html
   <script>
     window.onload = function() {
       if (window.SmartReportingTool) {
         const { App, React, ReactDOM, ChakraProvider } = window.SmartReportingTool;
         const config = {
           apiUrl: 'http://localhost:8000',
           // Add any other configuration options here
         };
         const container = document.getElementById('smart-reporting-tool-container');
         const root = ReactDOM.createRoot(container);
         root.render(
           React.createElement(ChakraProvider, null,
             React.createElement(App, { config: config })
           )
         );
       } else {
         console.error('Failed to initialize SmartReportingTool: SmartReportingTool not found');
       }
     };
   </script>
   ```

4. Ensure that your backend API is accessible from the domain where you're embedding the tool.

5. Customize the tool's appearance using CSS to match your website's design.

Note: Replace 'path/to/main.0a7877dd.js' with the actual path to the latest Smart Reporting Tool JavaScript file.

## Known Issues and Troubleshooting

- Minified React error #299: This error is related to React rendering issues and is currently being investigated.
- TypeError: Cannot read properties of undefined (reading 'default'): This error is related to module import problems and is being addressed.

If you encounter these issues, please check for updates in the repository or open an issue for assistance.

## Contributing

We welcome contributions to the Smart Reporting Tool! Please check back soon for detailed guidelines on how to contribute to this project.

## License

(License information will be added in the near future)
