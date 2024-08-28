import React, { useEffect, useRef, useState, useLayoutEffect } from 'react';
import Chart from 'chart.js/auto';
import { Box, Text } from '@chakra-ui/react';

const LineChart = ({ data }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  const containerRef = useRef(null);
  const [error, setError] = useState(null);

  useLayoutEffect(() => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect();
      console.log('Chart container dimensions after mount:', { width, height });
    }
  }, []);

useEffect(() => {
  console.log('LineChart useEffect triggered');
  console.log('LineChart data:', JSON.stringify(data, null, 2));

  const validateData = () => {
    if (!data || !Array.isArray(data.labels) || !Array.isArray(data.data)) {
      throw new Error('Invalid data format received');
    }
    if (data.labels.length === 0 || data.data.length === 0) {
      throw new Error('Empty data arrays received');
    }
    if (data.labels.length !== data.data.length) {
      throw new Error('Mismatched data and label array lengths');
    }
  };

  const createChart = () => {
    if (!chartRef.current) {
      throw new Error('Chart reference is not available');
    }

    const ctx = chartRef.current.getContext('2d');
    if (!ctx) {
      throw new Error('Failed to get 2D context from canvas');
    }

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const chartConfig = {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Sales',
          data: data.data,
          borderColor: 'rgb(30, 144, 255)',
          backgroundColor: 'rgba(30, 144, 255, 0.1)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(169, 169, 169, 0.2)' }
          },
          x: {
            grid: { color: 'rgba(169, 169, 169, 0.2)' }
          }
        },
        plugins: {
          legend: {
            labels: { color: 'rgb(105, 105, 105)' }
          }
        }
      }
    };

    chartInstance.current = new Chart(ctx, chartConfig);
    console.log('LineChart instance created');
  };

  try {
    validateData();
    createChart();
    setError(null);
  } catch (err) {
    console.error('Error in LineChart:', err);
    setError(err.message);
  }

  return () => {
    if (chartInstance.current) {
      console.log('Cleaning up chart instance');
      chartInstance.current.destroy();
    }
  };
}, [data]);

  if (error) {
    return (
      <Box width="100%" maxWidth="600px" bg="white" p={4} borderRadius="md" boxShadow="md">
        <Text color="red.500">Error: {error}</Text>
      </Box>
    );
  }

  return (
    <Box ref={containerRef} width="100%" maxWidth="600px" height="400px" bg="white" p={4} borderRadius="md" boxShadow="md">
      <canvas ref={chartRef}></canvas>
    </Box>
  );
};

export default LineChart;
