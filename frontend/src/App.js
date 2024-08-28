import React, { useState } from 'react';
import { ChakraProvider, Box, VStack, Grid, theme, Input, Button, Text, Spinner } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import axios from 'axios';

function SmartReportingApp() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResponse('');

    try {
      const result = await axios.post('http://localhost:8000/query', { text: query });
      setResponse(result.data.result);
    } catch (err) {
      setError('An error occurred while processing your query. Please try again.');
      console.error(err);
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
          </VStack>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default SmartReportingApp;
