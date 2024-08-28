import React, { useState, useRef } from 'react';
import { ChakraProvider, Box, VStack, Grid, theme, Input, Button, Text, Spinner, Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import axios from 'axios';
import LineChart from './components/LineChart';
import PieChart from './components/PieChart';

function SmartReportingApp() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [lineChartData, setLineChartData] = useState(null);
  const [pieChartData, setPieChartData] = useState(null);
  const [salesTableData, setSalesTableData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedChartType, setSelectedChartType] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResponse('');
    setLineChartData(null);
    setPieChartData(null);
    setSalesTableData(null);
    setSelectedChartType(null);

    try {
      console.log('Sending query:', query);
      const result = await axios.post('http://localhost:8000/query', { text: query });
      console.log('Received response:', result.data);
      if (result.data && result.data.result) {
        setResponse(result.data.result);

        // Analyze query to determine chart type
        const lowercaseQuery = query.toLowerCase();
        let chartType = result.data.chart_type || null;
        console.log('Chart type from backend:', chartType);
        if (!chartType) {
          if (lowercaseQuery.includes('trend') || lowercaseQuery.includes('over time')) {
            chartType = 'line';
          } else if (lowercaseQuery.includes('percentage') || lowercaseQuery.includes('share')) {
            chartType = 'pie';
          }
          console.log('Determined chart type from query:', chartType);
        }
        setSelectedChartType(chartType);

        console.log('Chart data from backend:', result.data.chart_data);
        console.log('Chart type:', chartType);
        if (chartType === 'line' && result.data.chart_data) {
          console.log('Setting line chart data:', result.data.chart_data);
          console.log('Line chart data structure:', JSON.stringify(result.data.chart_data, null, 2));
          setLineChartData({
            labels: result.data.chart_data.labels,
            data: result.data.chart_data.data
          });
        } else if (chartType === 'pie' && result.data.chart_data) {
          console.log('Setting pie chart data:', result.data.chart_data);
          console.log('Pie chart data structure:', JSON.stringify(result.data.chart_data, null, 2));
          setPieChartData(result.data.chart_data);
        } else {
          console.log('No matching chart type or data');
          console.log('Received chart type:', chartType);
          console.log('Received chart data:', result.data.chart_data);
        }

        if (result.data.sales_table) {
          console.log('Setting sales table data:', result.data.sales_table);
          setSalesTableData(result.data.sales_table);
        } else {
          console.log('No sales table data received');
        }
      } else {
        console.log('Unexpected response format:', result.data);
        setError('Received an unexpected response format. Please try again.');
      }
    } catch (err) {
      console.error('Error details:', err);
      setError('An error occurred while processing your query. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl" bg="gray.50">
        <Grid minH="100vh" p={3}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <VStack spacing={8}>
            <Text as="h1" fontSize="3xl" fontWeight="bold" color="blue.600">Welcome to Smart Reporting Tool</Text>
            <form onSubmit={handleSubmit}>
              <VStack spacing={4}>
                <Input
                  placeholder="Enter your query here"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  borderColor="blue.300"
                  _hover={{ borderColor: "blue.400" }}
                  _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px #3182ce" }}
                />
                <Button type="submit" colorScheme="blue" isLoading={isLoading}>
                  Submit Query
                </Button>
              </VStack>
            </form>
            {isLoading && <Spinner color="blue.500" />}
            {error && <Text color="red.500">{error}</Text>}
            {response && <Text color="gray.700">{response}</Text>}
            {selectedChartType === 'line' && lineChartData && (
              <LineChart data={lineChartData} />
            )}
            {selectedChartType === 'pie' && pieChartData && (
              <PieChart data={pieChartData} />
            )}
            {salesTableData && (
              <Box bg="white" p={4} borderRadius="md" boxShadow="md">
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th color="blue.600">Month</Th>
                      <Th isNumeric color="blue.600">Sales</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {salesTableData.map((row, index) => (
                      <Tr key={index} _hover={{ bg: "gray.50" }}>
                        <Td color="gray.700">{row.Month}</Td>
                        <Td isNumeric color="gray.700">{row.Sales}</Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            )}
          </VStack>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default SmartReportingApp;
