import React, { useState, useRef, useEffect } from 'react';
import { ChakraProvider, Box, VStack, Grid, theme, Input, Button, Text, Spinner, Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import axios from 'axios';
import Chart from 'chart.js/auto';

function SmartReportingApp() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [lineChartData, setLineChartData] = useState(null);
  const [salesTableData, setSalesTableData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (lineChartData && chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
      const ctx = chartRef.current.getContext('2d');
      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: lineChartData.labels,
          datasets: [{
            label: 'Sales',
            data: lineChartData.data,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }, [lineChartData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResponse('');
    setLineChartData(null);
    setSalesTableData(null);

    try {
      console.log('Sending query:', query);
      const result = await axios.post('http://localhost:8000/query', { text: query });
      console.log('Received response:', result.data);
      if (result.data && result.data.result) {
        setResponse(result.data.result);
        if (result.data.line_chart) {
          setLineChartData({
            labels: result.data.line_chart.labels,
            data: result.data.line_chart.data
          });
        }
        if (result.data.sales_table) {
          setSalesTableData(result.data.sales_table);
        }
      } else {
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
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <VStack spacing={8}>
            <h1>Welcome to Smart Reporting Tool</h1>
            <form onSubmit={handleSubmit}>
              <VStack spacing={4}>
                <Input
                  placeholder="Enter your query here"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <Button type="submit" colorScheme="blue" isLoading={isLoading}>
                  Submit Query
                </Button>
              </VStack>
            </form>
            {isLoading && <Spinner />}
            {error && <Text color="red.500">{error}</Text>}
            {response && <Text>{response}</Text>}
            {lineChartData && (
              <Box width="100%" maxWidth="600px">
                <canvas ref={chartRef}></canvas>
              </Box>
            )}
            {salesTableData && (
              <Table variant="simple">
                <Thead>
                  <Tr>
                    <Th>Month</Th>
                    <Th isNumeric>Sales</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {salesTableData.map((row, index) => (
                    <Tr key={index}>
                      <Td>{row.Month}</Td>
                      <Td isNumeric>{row.Sales}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            )}
          </VStack>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default SmartReportingApp;
